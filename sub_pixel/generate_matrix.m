%% Generate comparison matrix

function matrix = generate_matrix()

matrix = zeros(256,60);

for I = 1:256
   aux = generate_pattern(I);
   aux = ones(4,1)*aux;
   matrix(I, :) = (aux(:) - mean(aux(:)))/std(aux(:));
end

