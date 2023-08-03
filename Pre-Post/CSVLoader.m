function [Table] = CSVLoader(path, filename)

%% .csv Loader

AoA.Range       = 0:2:10;
AoA.Size        = max(size(AoA.Range));
loadfile        = readcell(strcat(path, filename));

% Pre-allocation
Alpha       = zeros(AoA.Size, 1);
CL          = zeros(AoA.Size, 1);
CDtot       = zeros(AoA.Size, 1);

for i = 1:AoA.Size

    Alpha(i)   = double(string(loadfile(5 + (40*(i-1)), 4)));
    CL(i)      = double(string(loadfile(16 + (40*(i-1)), 4)));
    CDtot(i)   = double(string(loadfile(11 + (40*(i-1)), 4)));

end

Table = horzcat(Alpha, CL, CDtot);