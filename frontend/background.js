// ============== TASK MANAGER CORE ==============
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
    chrome.runtime.sendMessage({ type: 'tasks_updated', tasks: this.tasks });
  }

  setupIcon() {
    chrome.action.setIcon({
      path: { "16": "icons/icon48.png", "32": "icons/icon48.png", "48": "icons/icon48.png" }
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
      const response = await fetch(this.API_ENDPOINTS.gemini, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: `Prioritize tasks as JSON:\n${
                this.tasks.map(t => `${t.id}||${t.text}`).join('\n')
              }\nRespond ONLY with: [{"id":"1","text":"task","priority":"high"}]`
            }]
          }]
        })
      });
      
      if (!response.ok) throw new Error(`API error: ${response.status}`);
      const data = await response.json();
      const resultText = data.candidates[0].content.parts[0].text;
      const prioritized = JSON.parse(resultText);
      this.tasks = prioritized;
      await this.saveTasks();
    } catch (error) {
      console.error('Prioritization failed:', error);
      this.tasks.forEach(t => t.priority = t.text.includes('!') ? 'high' : 'medium');
      this.saveTasks();
    }
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
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
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
    chrome.alarms.onAlarm.addListener(() => {
      const now = new Date();
      this.tasks.forEach(task => {
        if (task.dueDate && new Date(task.dueDate) < now) {
          chrome.notifications.create(`task-${task.id}`, {
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'Task Due',
            message: task.text,
            priority: 2
          });
        }
      });
    });
  }
}

// ============ INITIALIZATION ============
const taskManager = new TaskManager(); 
taskManager.init();
window.taskManager = taskManager;

// ============ MESSAGE HANDLER ============
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'addTask') taskManager.addTask(request.text).then(sendResponse);
  if (request.action === 'prioritizeTasks') taskManager.prioritizeTasks().then(sendResponse);
  if (request.action === 'scheduleTasks') taskManager.scheduleTasks().then(sendResponse);
  return true;
});