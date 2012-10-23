function file_contents = loadData(filename)
%READFILE reads a file and returns its entire contents 
%   file_contents = READFILE(filename) reads a file and returns its entire
%   contents in file_contents
%

% Load File
fid = fopen(filename);
if fid
    file_contents = fscanf(fid, '%d %d %d %d', [4, Inf])';
    fclose(fid);
else
    file_contents = '';
    fprintf('Unable to open %s\n', filename);
end

end

