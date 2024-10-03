try:
    from version import __version__, __author__, __author_email__
except ImportError:
    from .version import __version__, __author__, __author_email__

__all__ = [__version__, __author__, __author_email__]
