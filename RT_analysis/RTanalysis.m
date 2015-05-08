clear all
load population;
 sampleSize = size(unique(population(:,1)),1);
 NumTurns = 20;
 NumTrials = 30;
 TotalTrials = sampleSize*NumTrials;
 
 
 ExEx =[]; 
 Switch = [];
 RT= [];
%%%% to extract data from 2-20 turns from one trial 
 for i = 1 : TotalTrials
     WholeExEx = population((20*(i-1)+2):(20*(i-1)+20),4);
     WholeSwitch = population((20*(i-1)+2):(20*(i-1)+20),5);
     WholeRT = population((20*(i-1)+2):(20*(i-1)+20),7);
     
     ExEx = [ExEx;WholeExEx];
     Switch = [Switch; WholeSwitch];
     RT= [RT;WholeRT];
 end
 
 %%%to get the exact matching data
 ExploreTime =[];
 ExploitTime=[];
 SwitchTime=[];
 NonSwitchTime=[];
 SwitchToExploreTime = [];
 SwitchToExploitTime = [];
 size_SwitchToExploreTime =[];
 size_SwitchToExploitTime =[];
 
 total_size_explore_time = [];
 total_size_exploit_time = [];
 total_size_switch_time = [];
 total_szie_non_switch_time = [];
 total_size_switch_to_explore = [];
 total_size_switch_to_exploit = [];
 
 for i = 1 : sampleSize
      EachExEx = ExEx((570*(i-1)+1):(570*(i-1)+570),1);
      EachSwitch = Switch((570*(i-1)+1):(570*(i-1)+570),1);
      EachRT = RT((570*(i-1)+1):(570*(i-1)+570),1);
      
      
      EachExploreTime = sum(EachRT(EachExEx == 0))/size(EachRT(EachExEx == 0),1);
      EachExploitTime = sum(EachRT(EachExEx == 1))/size(EachRT(EachExEx == 1),1);
      
      total_size_explore_time = [total_size_explore_time; size(EachRT(EachExEx == 0),1)];
      total_size_exploit_time = [total_size_exploit_time; size(EachRT(EachExEx == 1),1)];
      
      EachSwitchTime =  sum(EachRT(EachSwitch == 1))/size(EachRT(EachSwitch == 1),1);
      EachNonSwitchTime = sum(EachRT(EachSwitch == 0))/size(EachRT(EachSwitch == 0),1);
      
      total_size_switch_time = [total_size_switch_time; size(EachRT(EachSwitch == 1),1)];
      total_szie_non_switch_time = [total_szie_non_switch_time; size(EachRT(EachSwitch == 0),1)];
      %%%%%%%%%%%%(EachSwitch == 1)&(EachExEx == 0): note this would return
      %%%%%%%%%%%%a same size of a matrix with logic value 0 or 1. and then
      %%%%%%%%%%%%matlab match it with the outside matrix's elements
      EachSwitchToExploreTime = sum(EachRT((EachSwitch == 1)&(EachExEx == 0)))/...
          size(EachRT((EachSwitch == 1)&(EachExEx == 0)),1);
      EachSwitchToExploitTime = sum(EachRT((EachSwitch == 1)&(EachExEx == 1)))/...
          size(EachRT((EachSwitch == 1)&(EachExEx == 1)),1);
      Eachsize_SwitchToExploreTime = size(EachRT((EachSwitch == 1)&(EachExEx == 0)),1);
      Eachsize_SwitchToExploitTime = size(EachRT((EachSwitch == 1)&(EachExEx == 1)),1);
      
       total_size_switch_to_explore = [total_size_switch_to_explore; Eachsize_SwitchToExploreTime];
       total_size_switch_to_exploit = [total_size_switch_to_exploit; Eachsize_SwitchToExploitTime];
      
 ExploreTime =[ExploreTime ; EachExploreTime];
 ExploitTime=[ExploitTime; EachExploitTime];
 SwitchTime=[SwitchTime;EachSwitchTime ];
 NonSwitchTime=[NonSwitchTime; EachNonSwitchTime];
 SwitchToExploreTime = [SwitchToExploreTime; EachSwitchToExploreTime];
 %%Nan means never swtich to explore again!!
 SwitchToExploitTime = [SwitchToExploitTime; EachSwitchToExploitTime];
 size_SwitchToExploreTime =[size_SwitchToExploreTime; Eachsize_SwitchToExploreTime];
 size_SwitchToExploitTime =[size_SwitchToExploitTime; Eachsize_SwitchToExploitTime];
 
 end
      %%%first, switch to exploration individual variatin
      %%second , weight the switch to exploration when compute the RT for
      %%switch to make it easy understanding
      mean(ExploreTime)
      std(ExploreTime)
      mean(ExploitTime)
      std(ExploitTime)
      mean(SwitchTime)
      std(SwitchTime)
      mean(NonSwitchTime)
      std(NonSwitchTime)
      mean(SwitchToExploreTime)
      mean(SwitchToExploreTime(~isnan(SwitchToExploreTime)))
      std(SwitchToExploreTime(~isnan(SwitchToExploreTime)))
      mean(SwitchToExploitTime)
      std(SwitchToExploitTime)
      %figure(1)
      %  hist(ExploreTime)
      %figure(2)
      %  hist(ExploitTime)
      %figure(3)
      %  hist(SwitchTime)
      %figure(4)
      %  hist(NonSwitchTime)
      s0 = SwitchToExploreTime(~isnan(SwitchToExploreTime));
      s1 = SwitchToExploitTime(~isnan(SwitchToExploreTime));
      %sT= (s0+s1)./2;
      %mean(sT)
      mean(s0)
      mean(s1)
      
      
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%switching_RT weighting algorithm
      
        weight_efficient = [sum(size_SwitchToExploreTime)/(sum(size_SwitchToExploreTime)...
            +sum(size_SwitchToExploitTime)) sum(size_SwitchToExploitTime)/...
            (sum(size_SwitchToExploreTime)...
            +sum(size_SwitchToExploitTime))];
        sT = [s0 s1] * weight_efficient';
        mean(sT);
      %%%%%%%histogram the times of switching to exploration
      figure()
      hist(size_SwitchToExploreTime);
      title('histogram of times of switching to exploration across 30 trials');
      
      %%%%%%%%%%%%%%%%%%%correlation between RTs and switch times of
      %%%%%%%%%%%%%%%%%%%backing to exploration
     [R, P] = corrcoef( [log(s0) log(size_SwitchToExploreTime(~isnan(SwitchToExploreTime)))])
     
     