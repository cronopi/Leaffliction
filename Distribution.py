#!/usr/bin/env python3
"""Analyse the distribution of a leaf image data set."""

import os
import sys

import matplotlib.pyplot as plt

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


def count_images(root):
    """Return {class_name: number_of_images} for every folder under root.

    class == directory that directly contains image files"""
    counts = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        n = sum(1 for f in filenames
                if f.lower().endswith(IMAGE_EXTENSIONS))
        if n > 0:
            name = os.path.basename(os.path.normpath(dirpath))
            counts[name] = counts.get(name, 0) + n
    return counts


def group_by_plant(counts):
    """Split {class: n} into {plant: {class: n}}.

    plant == class name before _"""
    plants = {}
    for name, n in sorted(counts.items()):
        plant = name.split("_")[0].capitalize()
        plants.setdefault(plant, {})[name] = n
    return plants


def plot_plant(plant, classes):
    names = list(classes.keys())
    values = list(classes.values())
    colors = plt.cm.tab10.colors[:len(names)]

    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"{plant} class distribution", fontsize=16)

    ax_pie.pie(values, labels=names, colors=colors,
               autopct="%1.1f%%", startangle=90)
    ax_pie.axis("equal")

    bars = ax_bar.bar(names, values, color=colors)
    ax_bar.bar_label(bars)
    ax_bar.set_ylabel("Number of images")
    ax_bar.tick_params(axis="x", rotation=30)
    ax_bar.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    return fig


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)
    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a directory")
        sys.exit(1)

    counts = count_images(root)
    if not counts:
        print(f"Error: no images found in '{root}'")
        sys.exit(1)

    for plant, classes in group_by_plant(counts).items():
        print(f"{plant}:")
        for name, n in classes.items():
            print(f"  {name:<20} {n}")
        plot_plant(plant, classes)
    plt.show()


if __name__ == "__main__":
    main()
