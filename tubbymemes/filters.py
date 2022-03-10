from flask import Blueprint
from arrow import get as arrow_get

from tubbymemes import config


bp = Blueprint('filters', 'filters')


@bp.app_template_filter('shorten_address')
def shorten_address(a):
    _p = a[0:6]
    _s = a[-4:]
    return f'{_p}...{_s}'


@bp.app_template_filter('humanize')
def humanize(d):
    if not d:
        return 'never'
    return arrow_get(d).humanize()

@bp.app_template_filter()
def show_snowtrace(s) -> str:
    """
    Return proper links to Etherscan based upon the currently configured network.
    """
    if config.CONTRACT_TESTNET:
        return f'https://testnet.snowtrace.io/search?f=0&q={s}'
    else:
        return f'https://snowtrace.io/search?f=0&q={s}'
