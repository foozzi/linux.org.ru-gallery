import argparse

from lor_gallery import LorGallery


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('--debug', help='debug mode', action='store_true')

    return parser


if __name__ == "__main__":
    args = create_parser()
    namespace = args.parse_args()

    debug = False

    if namespace.debug:
        debug = True

    lorgallery = LorGallery(debug=debug)
    lorgallery.get_list_archive()

