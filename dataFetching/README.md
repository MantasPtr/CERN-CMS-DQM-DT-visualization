# Module responsable for feching data from url

Main function in this module is ```dataLoader.async_fetch_all_data(identifier)``` which generates coroutine (because its async) that fetches data based on identifier and params. The url to fetch data from are generated in ```urlGenerator.py```.

Since url are certificate protected, ```authContainer.py``` contains information about the certificate and ```asyncRequestExecutor``` is responsible for making ssl protected request.

## async?

This module is async in order to more efficiently use resources when performing multiple request.
