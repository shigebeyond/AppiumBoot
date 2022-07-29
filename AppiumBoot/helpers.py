import os
import sys
from selenium.common.exceptions import InvalidSessionIdException
from sauceclient import SauceClient
from pyutilb import log

sauce = None
if os.getenv('SAUCE_LABS') and os.getenv('SAUCE_USERNAME') and os.getenv('SAUCE_ACCESS_KEY'):
    sauce = SauceClient(os.getenv('SAUCE_USERNAME'), os.getenv('SAUCE_ACCESS_KEY'))

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def take_screenshot_and_logcat(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'logcat')

def take_screenshot_and_syslog(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'syslog')

def __save_log_type(driver, device_logger, calling_request, type):
    logcat_dir = device_logger.logcat_dir
    screenshot_dir = device_logger.screenshot_dir

    try:
        driver.save_screenshot(os.path.join(screenshot_dir, calling_request + '.png'))
        logcat_data = driver.get_log(type)
    except InvalidSessionIdException:
        logcat_data = ''

    with open(os.path.join(logcat_dir, '{}_{}.log'.format(calling_request, type)), 'w') as logcat_file:
        for data in logcat_data:
            data_string = '%s:  %s\n' % (data['timestamp'], data['message'].encode('utf-8'))
            logcat_file.write(data_string)

def report_to_sauce(session_id):
    if sauce is not None:
        log.debug("Link to your job: https://saucelabs.com/jobs/%s" % session_id)
        passed = str(sys.exc_info() == (None, None, None))
        sauce.jobs.update_job(session_id, passed=passed)
    else:
        # this function gets called whether sauce is enabled or not.
        # if we get here, we weren't using sauce, so silently do nothing
        pass
