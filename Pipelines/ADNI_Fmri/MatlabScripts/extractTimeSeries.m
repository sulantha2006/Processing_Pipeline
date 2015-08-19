function time_series = extractTimeSeries(input_file, x, y, z, size)
% x, y, z need to be in world coordinates

%Adding paths
addpath('/home/wang/Documents/MATLAB/fmristat','-end');
addpath('/home/wang/Documents/MATLAB/emma','-end');

% World to Voxel
voxelW = [x y z];
h=openimage(input_file);
voxel = voxelW'; % To make worldtovoxel work
voxel = worldtovoxel(h,voxel,'xyzorder zerobase noflip');
voxel = round(voxel);
closeimage(h);

% Voxel Enlargment
x = voxel(1)-1:voxel(1)+size; % radius for seed 3x3x3voxels
y = voxel(2)-1:voxel(2)+size;
z = voxel(3)-1:voxel(3)+size;
[x,y,z] = meshgrid(x,y,z);
voxel = [x(:),y(:),z(:)]; % Inversed right there
voxel = voxel';

exclude = 4; % Number of time frames to skip first
ref_data=squeeze(extract(voxel,input_file));
time_series = mean(ref_data);
time_series = time_series(exclude+1:end)';

% Normalizing time_series around mean of 500
time_series = (time_series - mean(time_series))*500;