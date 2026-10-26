use crate::{catalog::{self, Game}, launcher};
use eframe::egui;
use std::{collections::HashMap, path::PathBuf};

pub struct DiscodoApp {
    games: Vec<Game>,
    selected: usize,
    search: String,
    executable_paths: HashMap<String, PathBuf>,
    status: String,
    language: String,
}

impl DiscodoApp {
    pub fn new() -> Self {
        Self {
            games: catalog::load_catalog(),
            selected: 0,
            search: String::new(),
            executable_paths: HashMap::new(),
            status: "Choose a game and select its executable to get started.".into(),
            language: "English".into(),
        }
    }

    fn filtered_indices(&self) -> Vec<usize> {
        let q = self.search.trim().to_lowercase();
        self.games.iter().enumerate()
            .filter(|(_, game)| q.is_empty()
                || game.name.to_lowercase().contains(&q)
                || game.genre.to_lowercase().contains(&q))
            .map(|(i, _)| i)
            .collect()
    }

    fn selected_game(&self) -> Option<&Game> {
        self.games.get(self.selected)
    }

    fn choose_executable(&mut self) {
        let chosen = rfd::FileDialog::new()
            .add_filter("Executable", &["exe", "bat", "sh", "app"])
            .pick_file();
        if let Some(path) = chosen {
            if let Some(game) = self.selected_game() {
                self.executable_paths.insert(game.id.clone(), path.clone());
                self.status = format!("Executable set: {}", path.display());
            }
        }
    }

    fn launch_selected(&mut self) {
        let Some(game) = self.selected_game() else { return };
        let Some(path) = self.executable_paths.get(&game.id).cloned() else {
            self.status = "Select the game's actual executable first.".into();
            return;
        };
        match launcher::launch_executable(&path) {
            Ok(_) => self.status = format!("Launched {}.", game.name),
            Err(error) => self.status = format!("Launch failed: {error:#}"),
        }
    }
}

impl eframe::App for DiscodoApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::TopBottomPanel::top("header").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.heading(egui::RichText::new("Discodo").size(25.0).strong()
                    .color(egui::Color32::from_rgb(135, 150, 255)));
                ui.label(egui::RichText::new("LAUNCHER").small().weak());
                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    egui::ComboBox::from_id_salt("language")
                        .selected_text(&self.language)
                        .show_ui(ui, |ui| {
                            ui.selectable_value(&mut self.language, "English".into(), "English");
                            ui.selectable_value(&mut self.language, "Русский".into(), "Русский");
                        });
                });
            });
        });

        egui::SidePanel::left("library")
            .resizable(true)
            .default_width(290.0)
            .show(ctx, |ui| {
                ui.heading(if self.language == "Русский" { "Библиотека" } else { "Library" });
                ui.add_space(8.0);
                ui.add(egui::TextEdit::singleline(&mut self.search)
                    .hint_text(if self.language == "Русский" { "Поиск игр..." } else { "Search games..." }));
                ui.add_space(8.0);
                egui::ScrollArea::vertical().show(ui, |ui| {
                    for index in self.filtered_indices() {
                        let game = &self.games[index];
                        let selected = self.selected == index;
                        let title = format!("{}\n{}", game.name, game.genre);
                        if ui.selectable_label(selected, title).clicked() {
                            self.selected = index;
                        }
                        ui.add_space(3.0);
                    }
                });
                ui.separator();
                ui.label(egui::RichText::new(format!("{} games", self.games.len())).weak().small());
            });

        egui::CentralPanel::default().show(ctx, |ui| {
            if let Some(game) = self.selected_game().cloned() {
                ui.add_space(14.0);
                ui.horizontal(|ui| {
                    let (rect, _) = ui.allocate_exact_size(
                        egui::vec2(116.0, 148.0), egui::Sense::hover());
                    ui.painter().rect_filled(rect, 12.0,
                        egui::Color32::from_rgb(game.cover_color[0], game.cover_color[1], game.cover_color[2]));
                    ui.painter().text(rect.center(), egui::Align2::CENTER_CENTER,
                        game.name.chars().take(18).collect::<String>(),
                        egui::FontId::proportional(16.0), egui::Color32::WHITE);

                    ui.vertical(|ui| {
                        ui.add_space(6.0);
                        ui.heading(egui::RichText::new(&game.name).size(29.0));
                        ui.label(egui::RichText::new(&game.genre).color(egui::Color32::from_rgb(145, 155, 190)));
                        ui.add_space(8.0);
                        ui.label(&game.description);
                        ui.add_space(8.0);
                        ui.label(format!("Steam App ID: {}", game.steam_app_id.as_deref().unwrap_or("Not listed")));
                    });
                });

                ui.add_space(28.0);
                ui.heading(if self.language == "Русский" { "Путь к игре" } else { "Game executable" });
                let current_path = self.executable_paths.get(&game.id)
                    .map(|p| p.display().to_string())
                    .unwrap_or_else(|| "No executable selected".into());
                ui.label(egui::RichText::new(current_path).weak());
                ui.horizontal(|ui| {
                    if ui.button(if self.language == "Русский" { "Выбрать EXE…" } else { "Choose EXE…" }).clicked() {
                        self.choose_executable();
                    }
                    if ui.add_enabled(self.executable_paths.contains_key(&game.id),
                        egui::Button::new(if self.language == "Русский" { "▶ Запустить" } else { "▶ Play" })).clicked() {
                        self.launch_selected();
                    }
                });

                ui.add_space(26.0);
                ui.separator();
                ui.heading(if self.language == "Русский" { "Интеграции" } else { "Integrations" });
                ui.label("Discord Rich Presence");
                ui.label("Configure your own Discord application Client ID in a future settings panel.");
                ui.label("This launcher does not spoof game identity or bypass Discord Quests.");
                ui.add_space(8.0);
                ui.label("Steam shortcuts");
                ui.label("Safe shortcut export with backup/validation is planned; no Steam files are modified yet.");
            } else {
                ui.centered_and_justified(|ui| { ui.label("No game selected."); });
            }
        });

        egui::TopBottomPanel::bottom("status").show(ctx, |ui| {
            ui.horizontal_wrapped(|ui| {
                ui.label(egui::RichText::new("STATUS").small().strong());
                ui.label(&self.status);
            });
        });
    }
}
