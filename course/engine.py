from subprocess import Popen, PIPE, TimeoutExpired, run, STDOUT
import os

import logging
logr = logging.getLogger('custom')


# saves content to file with given name
def save_as_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content.strip())


# execute file in docker container and return output as string
def call_docker(command, stop_endless_run_sh, file_name, save_file_path, timeout):
    container_name = file_name
    try:
        p = Popen([command, container_name, save_file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(timeout=timeout)
        if len(output) == 0:
            return err.decode('utf-8').strip()
        return output.decode('utf-8').strip()

    except TimeoutExpired as e:
        run([stop_endless_run_sh, container_name], stderr=STDOUT)
        logr.debug("Timeout: {}".format(e))
        return "ERROR!!! Code run process timed out."
    except Exception as e:
        logr.error("Error when running containter: {}".format(e))
        return "ERROR when running code in container"



# executes given code in a docker container
def run_in_docker(save_path, content, run_in_docker_sh_path, stop_endless_run_sh, file_name, timeout):
    save_file_path = os.path.join(save_path, file_name)
    save_as_file(save_file_path, content)

    return call_docker(run_in_docker_sh_path, stop_endless_run_sh, file_name, save_file_path, timeout)

# executes given code in a docker container
def run_python_in_docker(save_path, content, run_in_docker_sh_path, stop_endless_run_sh, file_name, timeout):
    save_file_path = os.path.join(save_path, file_name)
    save_as_file(save_file_path, content)

    command = run_in_docker_sh_path
    container_name = file_name
    try:
        p = Popen([command, container_name, save_file_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(timeout=timeout)
        if len(output) == 0:
            return err.decode('utf-8').strip()
        return output.decode('utf-8').strip()

    except TimeoutExpired as e:
        run([stop_endless_run_sh, container_name], stderr=STDOUT)
        logr.debug("Timeout: {}".format(e))
        return "ERROR!!! Code run process timed out."
    except Exception as e:
        logr.error("Error when running containter: {}".format(e))
        return "ERROR when running code in container"


# executes given code in a docker container
def run_c_in_docker(save_path, content, run_in_docker_sh_path, stop_endless_run_sh, file_name, timeout):
    save_file_path = os.path.join(save_path, file_name)

    print("IN C", content)
    print("save_path", save_path)

    print("save_file_path", save_file_path)

    save_as_file(save_file_path, content)

    output_name = os.path.splitext(file_name)[0]
    output_file_path = os.path.join(save_path, output_name)

    print('output_file_path', output_file_path)

    command = run_in_docker_sh_path
    container_name = file_name

    print('command', command)

    try:
        print("STARTING DOCKER.. C")
        p = Popen([command, container_name, save_file_path, save_path, file_name, output_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(timeout=timeout)
        # if len(output) == 0:
        #     return err.decode('utf-8').strip()
        # return output.decode('utf-8').strip()

        from subprocess import check_output
        foo = check_output(output_file_path, shell=True)

        print("OUT C", output)
        print("foo C", foo.decode('ascii'))

        return foo.decode('ascii')

    except TimeoutExpired as e:
        run([stop_endless_run_sh, container_name], stderr=STDOUT)
        logr.debug("Timeout: {}".format(e))
        return "ERROR!!! Code run process timed out."
    except Exception as e:
        logr.error("Error when running containter: {}".format(e))
        return "ERROR when running code in container"


# executes given code in a docker container
def run_java_in_docker(save_path, content, run_in_docker_sh_path, stop_endless_run_sh, file_name, timeout):
    save_file_path = os.path.join(save_path, file_name)

    print("IN JAVA", content)
    print("save_path", save_path)

    print("save_file_path", save_file_path)

    save_as_file(save_file_path, content)

    output_name = os.path.splitext(file_name)[0]
    output_file_path = os.path.join(save_path, output_name)

    print('output_file_path', output_file_path)

    command = run_in_docker_sh_path
    container_name = file_name

    print('command', command)

    try:
        print("STARTING DOCKER.. JAVA")
        p = Popen([command, container_name, save_file_path, save_path, file_name, output_name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(timeout=timeout)
        # if len(output) == 0:
        #     return err.decode('utf-8').strip()
        # return output.decode('utf-8').strip()

        print("OUT JAVA", output)

        from subprocess import check_output
        foo = check_output(output_file_path, shell=True)


        print("foo JAVA", foo.decode('ascii'))

        return foo.decode('ascii')

    except TimeoutExpired as e:
        run([stop_endless_run_sh, container_name], stderr=STDOUT)
        logr.debug("Timeout: {}".format(e))
        return "ERROR!!! Code run process timed out."
    except Exception as e:
        logr.error("Error when running containter: {}".format(e))
        return "ERROR when running code in container"