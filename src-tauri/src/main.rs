#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Serialize, Deserialize};
use std::fs;
use tauri::api::dialog::FileDialogBuilder;

#[derive(Serialize, Deserialize, Clone)]
struct Note {
    id: u64,
    title: String,
    content: String,
    tags: Vec<String>,
}

#[tauri::command]
fn get_notes() -> Result<Vec<Note>, String> {
    let path = tauri::api::path::app_data_dir(&tauri::Config::default()).unwrap().join("notes.json");
    if path.exists() {
        let data = fs::read_to_string(path).map_err(|e| e.to_string())?;
        Ok(serde_json::from_str(&data).unwrap_or(vec![]))
    } else {
        Ok(vec![])
    }
}

#[tauri::command]
fn save_notes(notes: Vec<Note>) -> Result<(), String> {
    let path = tauri::api::path::app_data_dir(&tauri::Config::default()).unwrap().join("notes.json");
    fs::create_dir_all(path.parent().unwrap()).map_err(|e| e.to_string())?;
    fs::write(path, serde_json::to_string(&notes).unwrap()).map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn export_html(content: String) -> Result<(), String> {
    let (tx, rx) = std::sync::mpsc::channel();
    FileDialogBuilder::new().add_filter("HTML", &["html"]).save_file(move |p| {
        if let Some(p) = p {
            let html = format!("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Note</title></head><body>{}</body></html>", content);
            let _ = fs::write(p, html);
        }
        let _ = tx.send(());
    });
    rx.recv().unwrap();
    Ok(())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_notes, save_notes, export_html])
        .run(tauri::generate_context!())
        .expect("error");
}
