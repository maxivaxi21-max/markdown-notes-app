# Markdown Note-Taking App

Кроссплатформенное приложение для создания заметок в Markdown с живым предпросмотром, тегами (упрощённо), поиском и экспортом в HTML. Реализовано на **Electron + React**, **Tauri + Svelte** и **Python + tkinter**.

## Возможности
- Редактор Markdown с подсветкой синтаксиса (CodeMirror)
- Живой HTML-предпросмотр справа
- Сохранение заметок в локальное хранилище (JSON / electron-store)
- Поиск по заголовкам
- Экспорт заметки в отдельный HTML-файл
- Тёмная / светлая тема

## Запуск

### Electron + React
```bash
cd electron-react
npm install
# терминал 1
npm run dev
# терминал 2
npm start
