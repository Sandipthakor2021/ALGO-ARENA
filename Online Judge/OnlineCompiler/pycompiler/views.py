from django.shortcuts import render
import sys
import io
import time
import tracemalloc


def index(request):
    return render(request, 'index.html')


def runcode(request):
    original_stdout = None
    output = None
    execution_time = 0
    memory_usage = 0
    memory_usage_mb = 0

    if request.method == "POST":
        codeareadata = request.POST['codearea']
        inputdata = request.POST.get('input', '')

        try:
            # Save original standard output reference
            original_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')  # Change the standard output to the file we created

            # Redirect stdin to the input string
            sys.stdin = io.StringIO(inputdata)

            # Record the current memory usage
            tracemalloc.start()

            # Start the timer
            start_time = time.time()

            # Execute code
            exec(codeareadata)  # Example --> print("hello world")

            # Stop the timer
            execution_time = time.time() - start_time

            sys.stdout.close()

            sys.stdout = original_stdout  # Resetting the standard output to its original value

            # Get the current memory usage
            current, peak = tracemalloc.get_traced_memory()
            memory_usage = peak - current

            # Convert the memory usage from bytes to megabytes
            memory_usage_mb = memory_usage / 10 ** 6

            # Finally, read output from file and save in output variable
            output = open('file.txt', 'r').read()

            # Add a message indicating success
            success_message = "Status: Correct Answer"
        except Exception as e:
            # To return error in the code
            sys.stdout = original_stdout
            output = e
            success_message = None

    # Finally, return and render the index page and then send code data and output to show on the page
    return render(request, 'index.html', {"code": codeareadata, "output": output, "execution_time": execution_time,
                                          "memory_usage": memory_usage, "memory_usage_mb": memory_usage_mb,
                                          "success_message": success_message})

