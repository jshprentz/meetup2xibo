"""Finds Xibo dataset IDs."""

from .exceptions import DatasetDiscoveryError


class XiboDatasetIdFinder:

    """Finds Xibo dataset IDs."""

    def __init__(self, xibo_api):
        """Initialize with a Xibo API."""
        self.xibo_api = xibo_api

    def find_dataset_id(self, dataset_code):
        """Find a dataset's ID given the dataset code configured in the Xibo
        CMS."""
        datasets = self.get_xibo_datasets(dataset_code)
        if len(datasets) == 1:
            return datasets[0]["dataSetId"]
        else:
            raise DatasetDiscoveryError(
                self.datasets_problem(dataset_code, datasets))

    def get_xibo_datasets(self, dataset_code):
        """Get a list of Xibo datasets given a dataset code."""
        return self.xibo_api.get_datasets_by_code(dataset_code)

    def datasets_problem(self, dataset_code, datasets):
        """Return a message describing the problem with the list of datasets
        for a dataset code."""
        if datasets:
            return self.multiple_dataset_problem(dataset_code, datasets)
        else:
            return 'No Xibo datasets had code "{}"'.format(dataset_code)

    @staticmethod
    def multiple_dataset_problem(dataset_code, datasets):
        """Return a message describing the multiple datasets for a dataset
        code."""
        list_summary = ",".join((
            "{} ({:d})".format(info["dataSet"], info["dataSetId"])
            for info in datasets))
        return "{:d} Xibo datasets had code {}: {}".format(
            len(datasets), dataset_code, list_summary)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
