use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Game {
    pub id: String,
    pub name: String,
    pub genre: String,
    pub description: String,
    pub executable_hint: String,
    pub steam_app_id: Option<String>,
    pub cover_color: [u8; 3],
}

pub fn load_catalog() -> Vec<Game> {
    serde_json::from_str(include_str!("../data/games.json"))
        .expect("Bundled data/games.json must contain a valid game array")
}
