addpath('jsonlab-2.0');
jsondata = loadjson('../Manifest.json');
videopath = jsondata.VideoPath;
videopath = ['../' videopath];
fps = jsondata.Fps;

start_sec = 53;
end_sec = 63;
