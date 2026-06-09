import React, { useState, useEffect } from 'react';
import { Controlled as CodeMirror } from 'react-codemirror2';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/material.css';
import 'codemirror/mode/markdown/markdown';
import { marked } from 'marked';

function App() {
  const [notes, setNotes] = useState([]);
  const [current, setCurrent] = useState({ id: null, title: '', content: '', tags: [] });
  const [search, setSearch] = useState('');
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    window.electronAPI.getNotes().then(data => {
      if (data.length) setNotes(data);
      else setNotes([{ id: Date.now(), title: 'Welcome', content: '# Hello\n\nStart typing...', tags: [] }]);
    });
  }, []);

  useEffect(() => { window.electronAPI.saveNotes(notes); }, [notes]);

  const saveCurrent = () => {
    if (current.id) setNotes(notes.map(n => n.id === current.id ? current : n));
    else setNotes([...notes, { ...current, id: Date.now() }]);
  };

  const exportAsHtml = async () => {
    const path = await window.electronAPI.saveDialog();
    if (path) {
      const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${current.title}</title></head><body>${marked(current.content)}</body></html>`;
      await window.electronAPI.exportHtml(html, path);
    }
  };

  const filtered = notes.filter(n => n.title.toLowerCase().includes(search.toLowerCase()));

  return (
    <div style={{ display: 'flex', height: '100vh', background: theme === 'dark' ? '#1e1e1e' : '#fff', color: theme === 'dark' ? '#ddd' : '#000' }}>
      <div style={{ width: 250, borderRight: '1px solid gray', padding: 10 }}>
        <button onClick={() => setCurrent({ id: null, title: '', content: '', tags: [] })}>+ New</button>
        <input placeholder="Search" value={search} onChange={e => setSearch(e.target.value)} style={{ width: '100%', margin: '10px 0' }} />
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {filtered.map(n => (
            <li key={n.id} style={{ cursor: 'pointer', margin: '5px 0', background: current.id === n.id ? '#555' : 'transparent' }} onClick={() => setCurrent(n)}>
              {n.title}
              <button onClick={() => setNotes(notes.filter(x => x.id !== n.id))}>🗑️</button>
            </li>
          ))}
        </ul>
        <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>Toggle theme</button>
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <input value={current.title} onChange={e => setCurrent({ ...current, title: e.target.value })} placeholder="Title" style={{ fontSize: 20, padding: 10 }} />
        <div style={{ display: 'flex', flex: 1 }}>
          <CodeMirror
            value={current.content}
            options={{ mode: 'markdown', theme: theme === 'dark' ? 'material' : 'default', lineNumbers: true }}
            onBeforeChange={(editor, data, value) => setCurrent({ ...current, content: value })}
            style={{ width: '50%' }}
          />
          <div style={{ width: '50%', overflow: 'auto', padding: 10, borderLeft: '1px solid gray' }} dangerouslySetInnerHTML={{ __html: marked(current.content) }} />
        </div>
        <div style={{ padding: 10 }}>
          <button onClick={saveCurrent}>Save</button>
          <button onClick={exportAsHtml}>Export HTML</button>
        </div>
      </div>
    </div>
  );
}

export default App;
