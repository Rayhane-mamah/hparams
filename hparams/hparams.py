from hparams.localconfig import LocalConfig
import io
from contextlib import redirect_stderr
import argparse
import os


class HParams(LocalConfig):
    _loaded_hparams_objects = {}

    def __init__(self, project_path, hparams_filename="hparams", name="hparams"):
        if name in HParams._loaded_hparams_objects.keys():
            raise ValueError(f"hparams {name} is being loaded a second time")

        # params_to_override = HParams.override_params()

        super(HParams, self).__init__()

        self.read(os.path.join(project_path, f"{hparams_filename}.cfg"))

        # self.update(params_to_override)

        logdir = os.path.join(project_path, 'logs-{}'.format(self.run.name))
        os.makedirs(logdir, exist_ok=True)
        logfile = os.path.join(logdir, 'hparams-{}.cfg'.format(self.run.name))

        if os.path.isdir(logdir) and os.path.isfile(logfile):
            # If logfile is found, assume we are resuming as old run, so use archived hparams file
            super(HParams, self).__init__()
            self.read(logfile)
            # self.update(params_to_override)
            print('Found existing {}! Resuming run using primary parameters!'.format(logfile))
        else:
            # New run
            # Keep a version of the updated config file as backup for replicability
            self.save_config(logfile)
            print('No existing config found. New run config file saved in {}'.format(logfile))

        self.add_to_global_collections(name)

    def add_to_global_collections(self, name):
        HParams._loaded_hparams_objects[name] = self

    @staticmethod
    def get_hparams_by_name(name):
        return HParams._loaded_hparams_objects[name]

    @staticmethod
    def override_params():
        try:
            f = io.StringIO()
            with redirect_stderr(f):
                parser = argparse.ArgumentParser()
                parser.add_argument('override_params', nargs='+')
                args = parser.parse_args()

            params = args.override_params
        except:
            params = None
        return params
