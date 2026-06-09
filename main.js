const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const Store = require('electron-store');

const store = new Store({ name: 'notes' });

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadURL('http://localhost:5173');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });

ipcMain.handle('get-notes', () => store.get('notes', []));
ipcMain.handle('save-notes', (event, notes) => store.set('notes', notes));
ipcMain.handle('export-html', async (event, content, filePath) => {
  fs.writeFileSync(filePath, content);
  return true;
});
ipcMain.handle('save-dialog', async () => {
  const result = await dialog.showSaveDialog({ filters: [{ name: 'HTML', extensions: ['html'] }] });
  return result.filePath;
});
