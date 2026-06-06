import argparse
import os
import shutil
import sys
from pathlib import Path

try:
    from ultralytics import YOLO
except ImportError:
    print("[train.py] ERROR: ultralytics is not installed. Run: pip install ultralytics")
    sys.exit(1)

DEFAULT_MODEL = "yolov8n.pt"
DEFAULT_OUTPUT = os.path.join("models", "radar_yolov8n.pt")


def write_data_yaml(train_dir: str, val_dir: str, nc: int, class_name: str, output_path: str) -> str:
    names = [class_name]
    content = (
        f"train: {train_dir}\n"
        f"val: {val_dir}\n"
        f"nc: {nc}\n"
        f"names: {names}\n"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a YOLOv8 model and export it as models/radar_yolov8n.pt"
    )
    parser.add_argument(
        "--train",
        required=True,
        help="Path to the folder containing training images and labels",
    )
    parser.add_argument(
        "--val",
        required=True,
        help="Path to the folder containing validation images and labels",
    )
    parser.add_argument(
        "--data",
        help="Optional YAML dataset file. If omitted, train.yml is generated from --train and --val",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Base YOLO model to fine-tune (default: yolov8n.pt)",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Destination path for the trained model file",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size for training",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=16,
        help="Batch size for training",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to use for training, e.g. cpu, cuda:0, or dml for DirectML/AMD if supported by your environment.",
    )
    parser.add_argument(
        "--class-name",
        default="radar",
        help="Name of the object class to detect",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.data:
        data_path = Path(args.data)
        if not data_path.is_file():
            print(f"[train.py] ERROR: Dataset YAML not found: {data_path}")
            sys.exit(1)
        data_path = str(data_path.resolve())
    else:
        train_dir = Path(args.train).resolve()
        val_dir = Path(args.val).resolve()
        if not train_dir.is_dir():
            print(f"[train.py] ERROR: Training directory not found: {train_dir}")
            sys.exit(1)
        if not val_dir.is_dir():
            print(f"[train.py] ERROR: Validation directory not found: {val_dir}")
            sys.exit(1)
        data_path = str(Path("data.yaml").resolve())
        write_data_yaml(str(train_dir), str(val_dir), 1, args.class_name, data_path)
        print(f"[train.py] Generated dataset config: {data_path}")

    output_dir = Path(args.output).resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[train.py] Training model: {args.model}")
    print(f"[train.py] Dataset YAML: {data_path}")
    print(f"[train.py] Output path: {args.output}")
    print(f"[train.py] Epochs: {args.epochs}, img size: {args.imgsz}, batch: {args.batch}")

    model = YOLO(args.model)

    # Check if using DirectML
    device = args.device
    if device.lower() == "dml":
        try:
            import torch_directml
            # Using torch_directml device.
            device = torch_directml.device()
            print(f"[train.py] Using DirectML on device: {device}")
        except ImportError:
            print("[train.py] ERROR: torch-directml is not installed. Run: pip install torch-directml")
            sys.exit(1)

    try:
        model.train(
            data=data_path,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            device=device,
            project="runs/train",
            name="radar_yolov8n",
            exist_ok=True,
        )
    except ValueError as exc:
        print(f"[train.py] ERROR: {exc}")
        print("[train.py] Use --device cpu to train on the CPU or run training on a CUDA-capable machine.")
        sys.exit(1)

    best_weight = Path("runs/train/radar_yolov8n/weights/best.pt")
    if not best_weight.exists():
        print(f"[train.py] ERROR: Expected trained weights not found at {best_weight}")
        sys.exit(1)

    shutil.copy(best_weight, args.output)
    print(f"[train.py] Copied trained model to {args.output}")
    print("[train.py] Training complete. Run: py vision_worker.py")


if __name__ == "__main__":
    main()
