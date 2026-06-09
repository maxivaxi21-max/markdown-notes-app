const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getNotes: () => ipcRenderer.invoke('get-notes'),
  saveNotes: (notes) => ipcRenderer.invoke('save-notes', notes),
  exportHtml: (content, path) => ipcRenderer.invoke('export-html', content, path),
  saveDialog: () => ipcRenderer.invoke('save-dialog'),
});
