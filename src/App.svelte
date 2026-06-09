<script>
  import { onMount } from 'svelte';
  import { invoke } from '@tauri-apps/api/tauri';
  import CodeMirror from 'svelte-codemirror-editor';
  import 'codemirror/lib/codemirror.css';
  import 'codemirror/theme/material.css';
  import 'codemirror/mode/markdown/markdown';
  import { marked } from 'marked';

  let notes = [];
  let current = { id: null, title: '', content: '', tags: [] };
  let search = '';
  let theme = 'dark';

  onMount(async () => {
    notes = await invoke('get_notes');
    if (notes.length) current = notes[0];
  });

  $: { invoke('save_notes', { notes }); }

  function saveCurrent() {
    if (current.id) {
      notes = notes.map(n => n.id === current.id ? current : n);
    } else {
      current.id = Date.now();
      notes = [...notes, current];
    }
  }

  async function exportHTML() {
    await invoke('export_html', { content: marked(current.content) });
  }
</script>

<div style="display: flex; height: 100vh; background: {theme === 'dark' ? '#1e1e1e' : '#fff'}; color: {theme === 'dark' ? '#ddd' : '#000'}">
  <div style="width: 250px; border-right: 1px solid gray; padding: 10px">
    <button on:click={() => current = { id: null, title: '', content: '' }}>+ New</button>
    <input bind:value={search} placeholder="Search" style="width: 100%; margin: 10px 0" />
    <ul style="list-style: none; padding: 0">
      {#each notes.filter(n => n.title.toLowerCase().includes(search.toLowerCase())) as note}
        <li style="cursor: pointer; margin: 5px 0; background: {current.id === note.id ? '#555' : 'transparent'}" on:click={() => current = note}>
          {note.title}
          <button on:click={() => notes = notes.filter(n => n.id !== note.id)}>🗑️</button>
        </li>
      {/each}
    </ul>
    <button on:click={() => theme = theme === 'dark' ? 'light' : 'dark'}>Toggle theme</button>
  </div>
  <div style="flex: 1; display: flex; flex-direction: column">
    <input bind:value={current.title} placeholder="Title" style="font-size: 20px; padding: 10px" />
    <div style="display: flex; flex: 1">
      <CodeMirror bind:value={current.content} options={{ mode: 'markdown', theme: theme === 'dark' ? 'material' : 'default', lineNumbers: true }} style="width: 50%" />
      <div style="width: 50%; overflow: auto; padding: 10px; border-left: 1px solid gray" class="preview" dangerouslySetInnerHTML={{ __html: marked(current.content) }} />
    </div>
    <div style="padding: 10px">
      <button on:click={saveCurrent}>Save</button>
      <button on:click={exportHTML}>Export HTML</button>
    </div>
  </div>
</div>
