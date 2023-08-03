clear;
clc;

%% Aircraft Results
% Only Wing , No Prop

Path.Drag = "C:\WORKINGSPACE\OpenVSP\AERODB\Drag_Calculation\";

Results.CBUAM       = CSVLoader(Path.Drag, "UAM.csv");
Results.OPPAV       = CSVLoader(Path.Drag, "OPPAV.csv");
Results.X57         = CSVLoader(Path.Drag, "NASA_X57.csv");
Results.NASATilt    = CSVLoader(Path.Drag, "NASA_RVLT_Tiltwing.csv");
Results.Heaviside   = CSVLoader(Path.Drag, "KittyHawk_Heaviside.csv");
Results.Cora        = CSVLoader(Path.Drag, "JOBY_S4.csv");
Results.Joby        = CSVLoader(Path.Drag, "Cora.csv");

%% Post Performance

AoAList = Results.CBUAM(:,1);

% CL, CD AOA
% plotter_0 = figure;
% axes1 = axes('Parent',plotter_0,'FontSize',20,'FontName','Times New Roman');
% box(axes1,'on');
% grid(axes1,'off');  
% hold(axes1,'all');
% set(gca, 'LineWidth', 1.5)
% set(gcf, 'OuterPosition', [100, 100, 600, 580])
% set(gcf, 'color', 'w')
% set(gca, 'color', 'w')
% ytickformat('%,.1f')
% xtickformat('%,.0f')
% ylim([0.00 1.5])
% yticks(linspace(0.00, 1.5, 6))
% xlim([-1.0 11])
% xticks(linspace(0.0, 10, 6))
% ylabel(['\fontname{times new roman}' 'C_L'], 'fontsize', 20);
% xlabel(['\fontname{times new roman}' 'AoA, deg.'], 'fontsize', 20);
% plot(AoAList, Results.CBUAM(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','o','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.OPPAV(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','^','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.X57(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','s','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.NASATilt(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','d','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.Heaviside(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','x','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.Cora(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','v','color','k','MarkerFaceColor','none'); hold on
% plot(AoAList, Results.Joby(:,2), ...
%     'LineStyle','-','LineWidth',1,'Marker','^','color','k','MarkerFaceColor','none'); hold on
%     yyaxis right
%     ylabel(['\fontname{times new roman}' 'C_D'], 'fontsize', 20); 
%     ax = gca;
%     ax.YAxis(1).Color = 'k';
%     ax.YAxis(2).Color = 'k';
%     ytickformat('%,.1f')
%     ylim([0.00 1.00])
%     yticks(linspace(0.00, 1, 6))
%     plot(AoAList, Results.CBUAM(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','o','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.OPPAV(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','^','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.X57(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','s','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.NASATilt(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','d','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.Heaviside(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','x','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.Cora(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','v','color','k','MarkerFaceColor','none'); hold on
%     plot(AoAList, Results.Joby(:,3), ...
%         'LineStyle','-','LineWidth',1,'Marker','^','color','k','MarkerFaceColor','none'); hold on
% legend('CB UAM', 'OPPAV', 'X57', 'NASATilt', 'Heaviside', 'Cora', 'Joby');
% legend('Box','off')

% AOA vs L/D
plotter_0 = figure;
axes1 = axes('Parent',plotter_0,'FontSize',20,'FontName','Times New Roman');
box(axes1,'on');
grid(axes1,'off');  
hold(axes1,'all');
set(gca, 'LineWidth', 1.5)
set(gcf, 'OuterPosition', [100, 100, 600, 580])
set(gcf, 'color', 'w')
set(gca, 'color', 'w')
ytickformat('%,.0f')
xtickformat('%,.0f')
% ylim([0.00 1.5])
% yticks(linspace(0.00, 1.5, 6))
% xlim([-1.0 11])
% xticks(linspace(0.0, 10, 6))
ylabel(['\fontname{times new roman}' 'C_L'], 'fontsize', 20);
xlabel(['\fontname{times new roman}' 'AoA, deg.'], 'fontsize', 20);
plot(AoAList, Results.CBUAM(:,2)./Results.CBUAM(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','o','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.OPPAV(:,2)./Results.OPPAV(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','^','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.X57(:,2)./Results.X57(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','s','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.NASATilt(:,2)./Results.NASATilt(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','d','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.Heaviside(:,2)./Results.Heaviside(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','x','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.Cora(:,2)./Results.Cora(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','v','color','k','MarkerFaceColor','none'); hold on
plot(AoAList, Results.Joby(:,2)./Results.Joby(:,3), ...
    'LineStyle','-','LineWidth',1,'Marker','+','color','k','MarkerFaceColor','none'); hold on
legend('CB UAM', 'OPPAV', 'X57', 'NASATilt', 'Heaviside', 'Cora', 'Joby');
legend('Box','off')

%% Drag Calculation
% AoA = 4 deg.







