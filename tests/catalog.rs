use discodo_launcher::catalog::load_catalog;

#[test]
fn bundled_catalog_has_thirty_games() {
    let games = load_catalog();
    assert_eq!(games.len(), 50);
}

#[test]
fn bundled_catalog_has_unique_ids_and_names() {
    let games = load_catalog();
    let mut ids = std::collections::HashSet::new();
    let mut names = std::collections::HashSet::new();

    for game in games {
        assert!(!game.id.trim().is_empty());
        assert!(!game.name.trim().is_empty());
        assert!(ids.insert(game.id), "duplicate game id");
        assert!(names.insert(game.name), "duplicate game name");
    }
}
