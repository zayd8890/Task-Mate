class TaskManager {
  constructor() {
    this.tasks = [];
    this.API_ENDPOINTS = {
      gemini: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCmLboUpVu9qRiaJQ6tf7FEHKwF8d1ypi8',
      calendar: 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    };
  }

  async init() {
    await this.loadTasks();
    this.setupAlarms();
    this.setupIcon(); // Added icon initialization
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

  // Added dynamic icon setup
  setupIcon() {
    chrome.action.setIcon({
      path: {
        "16": "icons/icon48.png",
        "32": "icons/icon48.png",
        "48": "icons/icon48.png"
      }
    });
  }

  addTask(text) {
    const newTask = {
      id: Date.now().toString(),
      text,
      createdAt: new Date().toISOString(),
      priority: 'medium'
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
    } catch (error) {
      console.error('Prioritization failed:', error);
      this.fallbackPrioritization();
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

  async scheduleTasks() {
    try {
      const token = await this.getAuthToken();
      if (!token) throw new Error('No calendar access');
      
      for (const task of this.tasks.filter(t => !t.scheduled)) {
        await this.createCalendarEvent(task, token);
        task.scheduled = true;
      }
      await this.saveTasks();
    } catch (error) {
      console.error('Scheduling failed:', error);
    }
  }

  async createCalendarEvent(task, token) {
    const event = {
      summary: task.text,
      description: `Created by TaskMate (Priority: ${task.priority})`,
      start: { dateTime: new Date().toISOString() },
      end: { dateTime: new Date(Date.now() + 3600000).toISOString() }
    };

    const response = await fetch(this.API_ENDPOINTS.calendar, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(event)
    });

    if (!response.ok) throw new Error(`Calendar API error: ${response.status}`);
    return response.json();
  }

  getAuthToken() {
    return new Promise((resolve) => {
      chrome.identity.getAuthToken({ interactive: true }, (token) => {
        if (chrome.runtime.lastError) {
          console.error('Auth error:', chrome.runtime.lastError);
          resolve(null);
        } else {
          resolve(token);
        }
      });
    });
  }

  setupAlarms() {
    chrome.alarms.create('task-reminder', { periodInMinutes: 60 });
    chrome.alarms.onAlarm.addListener(this.checkDueTasks.bind(this));
  }

  checkDueTasks() {
    const now = new Date();
    this.tasks.forEach(task => {
      if (task.dueDate && new Date(task.dueDate) < now) {
        this.sendNotification(task);
      }
    });
  }

  sendNotification(task) {
    chrome.notifications.create(`task-${task.id}`, {
      type: 'basic',
      iconUrl: 'icons/icon48.png', // Using your 48px icon
      title: 'Task Due',
      message: task.text,
      priority: 2
    });
  }
}

// Message handlers
const messageHandlers = {
  draft_email: async () => {
    const token = await taskManager.getAuthToken();
    // Gmail API implementation
  },
  
  web_search: async ({ query }) => {
    try {
      const response = await fetch(
        `https://www.googleapis.com/customsearch/v1?q=${encodeURIComponent(query)}&key=YOUR_API_KEY`
      );
      return await response.json();
    } catch (error) {
      console.error('Search failed:', error);
    }
  }
};

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  const handler = messageHandlers[request.action];
  if (handler) {
    handler(request).then(sendResponse);
    return true; // Required for async response
  }
});

// Initialize
const taskManager = new TaskManager();
taskManager.init();