import json
from pathlib import Path


def main() -> None:
    """Generate beatdowns.json with backblast contents."""
    # Paths
    root = Path(__file__).parent
    input_path = root / 'beatdowns.json'
    backblast_dir = root / 'backblasts'
    output_path = root.parent / 'f3_nation_test_utils' / 'resources' / 'beatdowns.json'

    # Read beatdowns.json
    with input_path.open() as f:
        beatdowns = json.load(f)

    # Replace backblast field with file contents
    for bd in beatdowns:
        backblast_file = bd.get('backblast')
        if backblast_file:
            backblast_path = backblast_dir / backblast_file
            if backblast_path.exists():
                with backblast_path.open() as bf:
                    bd['backblast'] = bf.read()
            else:
                bd['backblast'] = f'[missing backblast file: {backblast_file}]'

    # Write to output
    with output_path.open('w') as f:
        json.dump(beatdowns, f, indent=2)


if __name__ == '__main__':
    main()
