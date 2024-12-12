## MI classifier for online inference

### Release
2024/01/24: ver1 


### Requirements 
```
pip install onnx, onnxruntime, scipy
```

### Implementation

#### The package is called via class ```Module_Prediction```

#### Run ```example_classifer.py``` , either (1) with class ```Get_Example_Data``` to run with offline data, or (2) with your custom data streaming function intergrated to the App.

* ```Get_Example_Data``` aims to create an example (random) data including (sample, label), simply using the "offline data", which we already have. Note that, during online testing, we will get the "real-time data" 
directly from the App via FLEX+LSL.

* For (1), you need to install MNE library, and download the raw offline data (interval marker file & the extracted edf file), then change the directory arguments accordingly.

* For (2), using your App's data streaming function to fetch the data into inference module.

* Important: The onnx model is specific for each subject, and it can be stored locally or on Cloud (to be discussed), for now the model is not yet optimized. This implementation is for test the App intergration only. 

Below is example for simple inference script

```
import os
import pandas as pd
from classifier.infer import Module_Prediction

def main():

    # Step 1: Init the module
    mp = Module_Prediction(
        path_onnx = "/home/pham/bci/REPO/ml_summary/model_[F1]_[2.0-0.5].onnx",
        fs = 128,
        window  = 2.0,
        overlap = 0.5,
    )

    # Step 2: Get the trial data and Run prediction 
    # TO DO: replace with your streaming function 
    g = Get_Example_Data()
    i = 0
    while i < 9:
        sample, label, id_trial = g.get()
        pred = mp.predict(sample)
        print(f"trial: {id_trial}, label={label}, pred={pred}")
        i += 1



if __name__ == "__main__":
    main()

```



## Fix
error: ```RuntimeError: liblsl library '/home/pham/miniconda3/envs/onlinebci/lib/liblsl.so' found but could not be loaded - possible platform/architecture mismatch.```

```rm -f /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so*```
```pip uninstall pylsl```

- Download (to the cwd) ```liblsl-1.16.2-focal_amd64.deb``` from ```https://github.com/sccn/liblsl/releases```
- Extract: ```dpkg-deb -x liblsl-1.16.2-focal_amd64.deb lsl-extracted```
- Check .so file: ```find lsl-extracted -name "liblsl.so.1.16.2"``` 
- Copy to lib: ```cp lsl-extracted/usr/lib/liblsl.so* /home/pham/miniconda3/envs/onlinebci/lib/```
- link: ```ln -s /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so.1.16.2 /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so```
- link: ```ln -s /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so.1.16.2 /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so.2```
- final check: ```ls -l /home/pham/miniconda3/envs/onlinebci/lib/ | grep liblsl```
where it should be look like this:
```
lrwxrwxrwx  1 pham pham       57 Nov  6 11:45 liblsl.so -> /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so.1.16.2
-rw-r--r--  1 pham pham   923264 Nov  6 11:43 liblsl.so.1.16.2
lrwxrwxrwx  1 pham pham       57 Nov  6 11:45 liblsl.so.2 -> /home/pham/miniconda3/envs/onlinebci/lib/liblsl.so.1.16.2
```