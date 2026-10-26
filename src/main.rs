mod app;
mod catalog;
mod launcher;

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("Discodo_Launcher")
            .with_inner_size([1120.0, 740.0])
            .with_min_inner_size([820.0, 560.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Discodo_Launcher",
        options,
        Box::new(|cc| {
            let mut visuals = egui::Visuals::dark();
            visuals.window_rounding = egui::Rounding::same(12.0);
            visuals.panel_fill = egui::Color32::from_rgb(16, 18, 25);
            cc.egui_ctx.set_visuals(visuals);
            Ok(Box::new(app::DiscodoApp::new()))
        }),
    )
}
