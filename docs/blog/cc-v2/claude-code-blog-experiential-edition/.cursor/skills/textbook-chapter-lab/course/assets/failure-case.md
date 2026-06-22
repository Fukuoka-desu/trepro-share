# Failure Case

An agent received “clean this folder” with broad write access. It renamed 180 files, overwrote the index, and reported success without a dry-run or verification. Git was not initialized.
