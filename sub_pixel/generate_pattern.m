%%% Correlation pattern generation

function pattern = generate_pattern(id)

ID = double(de2bi(uint8(id), 8));
ID = ID(end:-1:1);

pattern = [ones(1,5), -1, ID(1:4), -1, ID(5:end)];
pattern(pattern == 0) = -1;