#!/usr/bin/env python3
from src.server import MatrixController
import sys
from yaml import safe_load


if __name__ == '__main__':
    print('Run main mode')
    with open('conf.yaml') as conf_file:
        config = safe_load(conf_file)
    matrixController = MatrixController(config=config)
    try:
        print('Press CTRL-C to stop.')
        print(sys.version)
        matrixController.run()

    except KeyboardInterrupt:
        sys.exit(0)
