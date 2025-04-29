class TaskManager {
  constructor() {
    this.tasks = [];
    this.API_ENDPOINTS = {
      gemini: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCmLboUpVu9qRiaJQ6tf7FEHKwF8d1ypi8',
      calendar: 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    };
    this.SCOPES = ['https://www.googleapis.com/auth/calendar'];
  }

  async init() {
    await this.loadTasks();
    this.setupAlarms();
    this.setupIcon();
  }

  async loadTasks() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(['tasks'], (result) => {
        this.tasks = result.tasks || [];
        resolve();
      });
    });
  }

  async saveTasks() {
    return new Promise((resolve) => {
      chrome.storage.sync.set({ tasks: this.tasks }, () => {
        this.sendUpdate();
        resolve();
      });
    });
  }

  sendUpdate() {
    chrome.runtime.sendMessage({
      type: 'tasks_updated',
      tasks: this.tasks
    });
  }

  setupIcon() {
    chrome.action.setIcon({
      path: {
        "16": "icons/icon48.png",
        "32": "icons/icon48.png",
        "48": "icons/icon48.png"
      }
    });
  }

  addTask(text, priority = 'medium') {
    const newTask = {
      id: Date.now().toString(),
      text,
      createdAt: new Date().toISOString(),
      priority: priority,
      scheduled: false
    };
    this.tasks.push(newTask);
    return this.saveTasks();
  }

  async prioritizeTasks() {
    try {
      const token = await this.getAuthToken();
      if (!token) throw new Error('No auth token');
      
      const response = await fetch(this.API_ENDPOINTS.gemini, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `Prioritize tasks as JSON:\n${
                this.tasks.map(t => `${t.id}||${t.text}`).join('\n')
              }\nFormat: [{id, text, priority: "high/medium/low"}]`
            }]
          }]
        })
      });

      if (!response.ok) throw new Error(`API error: ${response.status}`);
      
      const data = await response.json();
      const resultText = data.candidates[0].content.parts[0].text;
      const prioritized = this.safeParse(resultText);
      
      this.tasks = prioritized;
      await this.saveTasks();
      return true;
    } catch (error) {
      console.error('Prioritization failed:', error);
      this.fallbackPrioritization();
      return false;
    }
  }

  safeParse(jsonString) {
    try {
      return JSON.parse(jsonString);
    } catch (e) {
      console.warn('Failed to parse AI response, using fallback');
      return this.tasks.map(t => ({
        ...t,
        priority: t.priority || 'medium'
      }));
    }
  }

  fallbackPrioritization() {
    this.tasks.forEach(t => {
      t.priority = t.text.includes('!') ? 'high' : 'medium';
    });
    this.saveTasks();
  }

  /**
   * Schedule tasks to Google Calendar
   * @returns {Promise<boolean>}
   */
  async scheduleTasks() {
    try {
      // Request calendar permissions with proper scopes
      const token = await this.getAuthToken(this.SCOPES);
      if (!token) {
        console.error('Calendar access denied');
        return false;
      }
      
      const tasksToSchedule = this.tasks.filter(t => !t.scheduled);
      if (tasksToSchedule.length === 0) {
        console.log('No tasks to schedule');
        return true;
      }

      for (const task of tasksToSchedule) {
        try {
          const eventResult = await this.createCalendarEvent(task, token);
          if (eventResult && eventResult.id) {
            task.scheduled = true;
            task.calendarEventId = eventResult.id;
            task.calendarLink = eventResult.htmlLink;
            console.log(`Task scheduled: ${task.text}`);
          }
        } catch (err) {
          console.error(`Failed to schedule task ${task.id}:`, err);
        }
      }
      
      await this.saveTasks();
      return true;
    } catch (error) {
      console.error('Scheduling failed:', error);
      return false;
    }
  }

  /**
   * Create a calendar event for a task
   * @param {Object} task - The task to schedule
   * @param {string} token - OAuth token
   * @returns {Promise<Object>} - Calendar event response
   */
  async createCalendarEvent(task, token) {
    // Default to scheduling based on priority
    let startTime;
    const now = new Date();
    
    switch(task.priority) {
      case 'high':
        // High priority: Schedule within 24 hours
        startTime = new Date(now.getTime() + 1000 * 60 * 60 * 3); // 3 hours from now
        break;
      case 'medium':
        // Medium priority: Schedule within 2-3 days
        startTime = new Date(now.getTime() + 1000 * 60 * 60 * 24 * 2); // 2 days from now
        break;
      case 'low':
        // Low priority: Schedule within a week
        startTime = new Date(now.getTime() + 1000 * 60 * 60 * 24 * 5); // 5 days from now
        break;
      default:
        startTime = new Date(now.getTime() + 1000 * 60 * 60 * 24); // 1 day from now
    }
    
    // Business hours adjustment (9 AM - 5 PM)
    startTime.setHours(9 + Math.floor(Math.random() * 8)); // Random hour between 9-17
    startTime.setMinutes(0);
    
    const endTime = new Date(startTime.getTime() + 3600000); // 1 hour duration
    
    // Prepare calendar event data
    const event = {
      summary: task.text,
      description: `Task created by TaskMate\nPriority: ${task.priority}`,
      start: { 
        dateTime: startTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      end: { 
        dateTime: endTime.toISOString(),
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      reminders: {
        useDefault: false,
        overrides: [
          { method: 'popup', minutes: 30 },
          { method: 'email', minutes: 60 }
        ]
      }
    };

    // Send request to Google Calendar API
    const response = await fetch(this.API_ENDPOINTS.calendar, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(event)
    });

    // Handle response
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Calendar API error:', response.status, errorData);
      
      // Handle token expiration
      if (response.status === 401) {
        // Invalidate the token so it will be refreshed next time
        chrome.identity.removeCachedAuthToken({ token });
        throw new Error('Auth token expired');
      }
      
      throw new Error(`Calendar API error: ${response.status}`);
    }
    
    return response.json();
  }

  /**
   * Get an OAuth token with the specified scopes
   * @param {Array<string>} scopes - OAuth scopes to request
   * @param {boolean} interactive - Whether to show login UI
   * @returns {Promise<string|null>} - The auth token or null
   */
  getAuthToken(scopes = [], interactive = true) {
    return new Promise((resolve) => {
      chrome.identity.getAuthToken({ 
        interactive: interactive,
        scopes: scopes
      }, (token) => {
        if (chrome.runtime.lastError) {
          console.error('Auth error:', chrome.runtime.lastError);
          resolve(null);
        } else {
          resolve(token);
        }
      });
    });
  }

  /**
   * Check if user is authenticated with calendar scope
   * @returns {Promise<boolean>}
   */
  async isAuthenticated() {
    const token = await this.getAuthToken(this.SCOPES, false);
    return !!token;
  }

  setupAlarms() {
    chrome.alarms.create('task-reminder', { periodInMinutes: 60 });
    chrome.alarms.onAlarm.addListener(this.handleAlarms.bind(this));
  }

  handleAlarms(alarm) {
    if (alarm.name === 'task-reminder') {
      this.checkDueTasks();
    }
  }

  checkDueTasks() {
    const now = new Date();
    const tasks = this.tasks.filter(task => 
      task.scheduled && task.calendarEventId && 
      new Date(task.createdAt).getTime() + 24 * 60 * 60 * 1000 < now.getTime()
    );
    
    tasks.forEach(task => {
      this.sendNotification(task);
    });
  }

  sendNotification(task) {
    chrome.notifications.create(`task-${task.id}`, {
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: 'Task Reminder',
      message: task.text,
      priority: 2
    });
  }

  /**
   * Delete a task by ID
   * @param {string} taskId 
   * @returns {Promise<boolean>}
   */
  async deleteTask(taskId) {
    const taskIndex = this.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) return false;
    
    const task = this.tasks[taskIndex];
    
    // If scheduled in calendar, delete the event
    if (task.scheduled && task.calendarEventId) {
      try {
        await this.deleteCalendarEvent(task);
      } catch (err) {
        console.error('Failed to delete calendar event:', err);
      }
    }
    
    this.tasks.splice(taskIndex, 1);
    await this.saveTasks();
    return true;
  }

  /**
   * Delete a calendar event
   * @param {Object} task 
   * @returns {Promise<boolean>}
   */
  async deleteCalendarEvent(task) {
    if (!task.calendarEventId) return false;
    
    try {
      const token = await this.getAuthToken(this.SCOPES);
      if (!token) return false;
      
      const url = `${this.API_ENDPOINTS.calendar}/${task.calendarEventId}`;
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      return response.ok || response.status === 404;
    } catch (err) {
      console.error('Delete calendar event error:', err);
      return false;
    }
  }

  /**
   * Schedule a single task to calendar
   * @param {string} taskId 
   * @returns {Promise<Object>}
   */
  async scheduleTask(taskId) {
    const task = this.tasks.find(t => t.id === taskId);
    if (!task) {
      return { success: false, error: 'Task not found' };
    }
    
    if (task.scheduled) {
      return { success: false, error: 'Task already scheduled' };
    }
    
    try {
      const token = await this.getAuthToken(this.SCOPES);
      if (!token) {
        return { success: false, error: 'Calendar access denied' };
      }
      
      const eventResult = await this.createCalendarEvent(task, token);
      if (eventResult && eventResult.id) {
        task.scheduled = true;
        task.calendarEventId = eventResult.id;
        task.calendarLink = eventResult.htmlLink;
        await this.saveTasks();
        return { 
          success: true, 
          eventLink: eventResult.htmlLink,
          task: task
        };
      }
      
      return { success: false, error: 'Failed to create calendar event' };
    } catch (error) {
      console.error('Schedule task failed:', error);
      return { success: false, error: error.message };
    }
  }
}