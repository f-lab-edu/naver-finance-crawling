import time


def infinite_scroll(driver, wait_time=1.5, max_scroll=100):
    scroll_count = 0
    while scroll_count < max_scroll:
        prev_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(wait_time)
        current_height = driver.execute_script("return document.body.scrollHeight")
        if prev_height == current_height:
            break

        scroll_count += 1
