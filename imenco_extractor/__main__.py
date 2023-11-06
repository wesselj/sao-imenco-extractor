from imenco_extractor import __version__
from imenco_extractor.extractor import extractor


def main() -> None:
    with extractor:
        extractor.run()


if __name__ == "__main__":
    main()
