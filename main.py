import argparse
import random
import os
import sounddevice as sd
import soundfile as sf


def main():
    parser = argparse.ArgumentParser(description="Who's That Pokemon?")
    parser.add_argument(
        "-g",
        "--gen",
        type=int,
        choices=range(1, 10),
        help="Specify the Pokemon generation (1-9)",
    )
    parser.add_argument(
        "-r", "--replay", action="store_true", help="Replay the last cry"
    )
    parser.add_argument(
        "-s", "--show", action="store_true", help="Show the last Pokemon"
    )
    parser.add_argument(
        "-d",
        "--sounddevice",
        nargs="?",
        type=int,
        const=-1,
        help="Show sound devices or specify device index to use",
    )

    args = parser.parse_args()

    if args.sounddevice is not None:
        devices = sd.query_devices()
        if args.sounddevice == -1:
            for idx, dev in enumerate(devices):
                print(f"{idx}: {dev['name']}")
            return
        else:
            device_idx = args.sounddevice
            if device_idx < 0 or device_idx >= len(devices):
                print("Invalid sound device index.")
                return
            sd.default.device = device_idx

    last_txt = "./last.txt"

    if args.replay:
        try:
            with open(last_txt, "r") as f:
                audio_path = f.read().strip()
            if not os.path.isfile(audio_path):
                print(f"Last file '{audio_path}' not found.")
                return
            poke_id = os.path.splitext(os.path.basename(audio_path))[0]
            print(f"Replaying Pokemon ID: {poke_id}")
        except Exception as e:
            print(f"Could not replay last cry: {e}")
            return
    else:
        if args.gen:
            gen = args.gen
            cries_dir = f"./cries/gen {gen}/"
            files = [
                f
                for f in os.listdir(cries_dir)
                if os.path.isfile(os.path.join(cries_dir, f))
            ]
            if not files:
                print(f"No cries found in {cries_dir}")
                return
            chosen_file = random.choice(files)
            poke_id = os.path.splitext(chosen_file)[0]
            audio_path = os.path.join(cries_dir, chosen_file)
        else:
            base_dir = "./cries/"
            all_files = []
            for folder in os.listdir(base_dir):
                folder_path = os.path.join(base_dir, folder)
                if os.path.isdir(folder_path):
                    files = [
                        os.path.join(folder, f)
                        for f in os.listdir(folder_path)
                        if os.path.isfile(os.path.join(folder_path, f))
                    ]
                    all_files.extend(files)
            if not all_files:
                print("No cries found in any generation folder.")
                return
            chosen_file = random.choice(all_files)
            poke_id = os.path.splitext(os.path.basename(chosen_file))[0]
            audio_path = os.path.join(base_dir, chosen_file)

        # Store last played file path
        with open(last_txt, "w") as f:
            f.write(audio_path)

        print(f"Selected Pokemon ID: {poke_id}")

    # Play the selected audio file
    data, samplerate = sf.read(audio_path)
    sd.play(data, samplerate)
    sd.wait()


if __name__ == "__main__":
    main()
