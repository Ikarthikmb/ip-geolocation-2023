% ECE 547
% Geolocation Project
% Marcel McCormick, Shree Woodradi, Karthik Banakar, Josue Gutierrez

clc
clear all
close all

data = readtable('geolocation_data');
x = data{:, 5};
y = data{:, 6};

figure (1)
plot(x, y, 'o')
hold on

centroid_x = sum(x)/numel(x);
centroid_y = sum(y)/numel(y);
plot(centroid_x, centroid_y, 'or')
hold off