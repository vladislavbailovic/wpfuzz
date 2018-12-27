import glob

def get_next_php_file(source):
    for phpfile in glob.glob(source + "**/*.php", recursive=True):
        with open(phpfile, 'r') as f:
            yield f

def get_ajax_action_from_line(line):
    if line.find('wp_ajax') == -1:
        return None

    start = line.find("wp_ajax_")
    end = line.find("'", start)
    ajax_call = ""
    if end == -1:
        end = line.find('"', start)
    if end > 0 and end > start:
        ajax_call = line[start:end]

    if ajax_call[-1] != '_' and -1 == ajax_call.find("%s"):
        return ajax_call.replace("wp_ajax_", "", 1).replace("nopriv_", "", 1)

    return None

def get_ajax(source_dir):
    ajax_calls = []
    for f in get_next_php_file(source_dir):
        for line in f.readlines():
            action = get_ajax_action_from_line(line)
            if action:
                ajax_calls.append(action)

    return ajax_calls
