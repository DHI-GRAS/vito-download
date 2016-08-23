from zipfile import ZipFile

def extract_h5(zipfname, outdir):
    """Extract the first h5 archive found in zipfname to outdir"""
    h5fname = None
    with ZipFile(zipfname, 'r') as zf:
        for member in zf.infolist():
            if member.filename.endswith("h5"):
                h5fname = zf.extract(member, outdir)
                break
    if h5fname is None:
        raise IOError('Unable to find \'h5\' data in zip file {}.'.format(zipfname))
    return h5fname
