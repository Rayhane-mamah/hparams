from hparams.localconfig import LocalConfig
import io
from contextlib import redirect_stderr
import argparse
import os
import gcsfs


class HParams(LocalConfig):
    _loaded_hparams_objects = {}

    def __init__(self, project_path, hparams_filename="hparams", gcs_backup_project=None, gcs_backup_bucket=None, name="hparams"):
        if name in HParams._loaded_hparams_objects.keys():
            raise ValueError(f"hparams {name} is being loaded a second time")

        # params_to_override = HParams.override_params()

        super(HParams, self).__init__()

        if gcs_backup_project is not None:
            if gcs_backup_bucket is None:
                raise ValueError(f"GCS bucket must be provided to conduct gcs backup!")

            if not gcs_backup_bucket.startswith('gs://'):
                gcs_backup_bucket = 'gs://' + gcs_backup_bucket

            gcs_fs = gcsfs.GCSFileSystem(project=gcs_backup_project)
            gcs_backup_bucket = gcs_backup_bucket

        else:
            gcs_fs = None

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

        if gcs_fs is not None:
            gcs_path = os.path.join(gcs_backup_bucket, os.path.basename(logfile))
            print(f'Backing up hparams file to {gcs_path}')
            gcs_fs.put(lpath=logfile, rpath=gcs_path)

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
