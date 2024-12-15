Installing osu.py
#################

.. code:: shell

    # Installs the latest version out on pypi

    # Linux/macOS
    python3 -m pip install -U osu.py

    # Windows
    py -3 -m pip install -U osu.py

    # Installing straight from github (downloads latest code, which is not guaranteed to be stable)
    py -m pip install git+https://github.com/Sheepposu/osu.py.git

    # Install with asynchronous client
    py -m pip install -U osu.py[async]
    # Install with all features
    py -m pip install -U osu.py[async,replay,notifications]

    # Install from github with features
    git clone https://github.com/sheppsu/osu.py
    cd osu.py
    py -m pip install -U .[async,replay,notifications]