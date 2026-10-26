use anyhow::{bail, Context, Result};
use std::{path::Path, process::{Child, Command}};

pub fn launch_executable(path: &Path) -> Result<Child> {
    if !path.is_file() {
        bail!("The selected executable does not exist: {}", path.display());
    }

    let working_dir = path.parent()
        .context("Could not determine executable working directory")?;

    Command::new(path)
        .current_dir(working_dir)
        .spawn()
        .with_context(|| format!("Failed to launch {}", path.display()))
}
