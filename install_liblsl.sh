#!/bin/bash

# Remember the current directory
current_dir=$(pwd)

# Step 1: Check if the repository is already cloned
repo_dir="../liblsl"
if [ ! -d "$repo_dir" ]; then
    echo "Repository not found. Cloning the repository."
    cd ..
    git clone https://github.com/sccn/liblsl
else
    echo "Repository already exists."
    cd "$repo_dir"
fi

# Step 2: Run the script in the repository
cd liblsl

# On Arch Linux,
# Uncomment the following line if needed:
# sudo pacman -S --needed base-devel cmake git

# Run the standalone compilation script
sudo ./standalone_compilation_linux.sh

# Step 3: Check if liblsl.so is present
if [[ -f "liblsl.so" ]]; then
    liblsl_path=$(realpath liblsl.so)
    
    # Check if the current shell is zsh or bash
    if [[ $SHELL == *"zsh"* ]]; then
        echo "export PYLSL_LIB=$liblsl_path" >> ~/.zshrc
        # Load the new environment variable for the current session
        source ~/.zshrc
        echo "liblsl.so path added to ~/.zshrc"
    elif [[ $SHELL == *"bash"* ]]; then
        echo "export PYLSL_LIB=$liblsl_path" >> ~/.bashrc
        # Load the new environment variable for the current session
        source ~/.bashrc
        echo "liblsl.so path added to ~/.bashrc"
    else
        echo "Unknown shell. Please manually add 'export PYLSL_LIB=$liblsl_path' to your shell's config."
    fi
else
    echo "liblsl.so not found. Compilation might have failed."
fi

# Go back to the original folder
cd "$current_dir"

echo "Setup complete."
