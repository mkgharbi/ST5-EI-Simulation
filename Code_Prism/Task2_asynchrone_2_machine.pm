dtmc

const double p1 = 0.1;
const double p2 = 0.1;

const double r1 = 0.5;
const double r2 = 0.5;

const int cap0 = 2;
const int cap1 = 25;
const int cap2 = 2;

const int timer = 100;

module control

phase : [1..2] init 1;

[phase1] phase=1 -> (phase'=2);
[phase2] phase=2 -> (phase'=1);

endmodule

const int buf0 = 1;

module buffer1

buf1 : [0..cap1] init 0;

[phase2] (pop1 & push1) | (!pop1 & !push1) -> (buf1'=buf1);
[phase2] !pop1 & push1 & buf1 < cap1 -> (buf1'=buf1+1);
[phase2] pop1 & !push1 & buf1 > 0 -> (buf1'=buf1-1);

endmodule

const int buf2 = 1;


module machine1

pop0 : bool init false;
push1 : bool init false;
is_up1: [0..1] init 1;

[phase1] is_up1=1 & (buf1<cap1 & buf0>0) -> p1:(is_up1'=0)&(pop0'=true)&(push1'=false) + (1-p1):(is_up1'=1)&(pop0'=true)&(push1'=true);
[phase1] is_up1=0 -> r1:(is_up1'=1)&(pop0'=false)&(push1'=true) + (1-r1):(is_up1'=0)&(pop0'=false)&(push1'=false);
[phase1] is_up1=1 & (buf0=0 | buf1=cap1) -> (is_up1'=1)&(pop0'=false)&(push1'=false);

[phase2] true -> (pop0'=false)&(push1'=false);

endmodule


module machine2

pop1 : bool init false;
push2 : bool init false;
is_up2: [0..1] init 1;

[phase1] is_up2=1 & (buf2<cap2 & buf1>0) -> p2:(is_up2'=0)&(pop1'=true)&(push2'=false) + (1-p2):(is_up2'=1)&(pop1'=true)&(push2'=true);
[phase1] is_up2=0 -> r2:(is_up2'=1)&(pop1'=false)&(push2'=true) + (1-r2):(is_up2'=0)&(pop1'=false)&(push2'=false);
[phase1] is_up2=1 & (buf1=0 | buf2=cap2) -> (is_up2'=1)&(pop1'=false)&(push2'=false);

[phase2] true -> (pop1'=false)&(push2'=false);

endmodule

// REWARDS
rewards "WIP"
	phase=1: 2 + buf1 - is_up1 - is_up2;
endrewards

rewards "Consumption"
	phase=2&pop0: 1;
endrewards

rewards "Production"
	phase=2&push2: 1;
endrewards

rewards "Production_rate"
	phase=2&push2: 2/timer;
endrewards

rewards "Starved2"
	phase=1&buf1=0: 2/timer;
endrewards

rewards "Blocked1"
	phase=1&buf1=cap1: 2/timer;
endrewards

rewards "Broken1"
	phase=1&is_up1=0: 2/timer;
endrewards

rewards "Broken2"
	phase=1&is_up2=0: 2/timer;
endrewards