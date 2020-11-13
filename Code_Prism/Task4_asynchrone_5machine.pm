dtmc

const double p1 =0.1;
const double p2 =0.1;
const double p3 =0.1;
const double p4 =0.1;
const double p5 =0.1;

const double r1 =0.5;
const double r2 =0.5;
const double r3 =0.5;
const double r4 =0.5;
const double r5 =0.5;

const int cap1= taille_buffer;
const int cap2= taille_buffer;
const int cap3= taille_buffer;
const int cap4= taille_buffer;
const int cap5= taille_buffer;

const int pallets = 8;

const int timer = 200;

const int taille_buffer;

module control

phase : [1..2] init 1;

[phase1] phase=1 -> (phase'=2);
[phase2] phase=2 -> (phase'=1);

endmodule


module buffer1

buf1 : [0..cap1] init 0;

[phase2] (pop1 & push1) | (!pop1 & !push1) -> (buf1'=buf1);
[phase2] !pop1 & push1 & buf1 < cap1 -> (buf1'=buf1+1);
[phase2] pop1 & !push1 & buf1 > 0 -> (buf1'=buf1-1);

endmodule


module buffer2

buf2 : [0..cap2] init 0;

[phase2] (pop2 & push2) | (!pop2 & !push2) -> (buf2'=buf2);
[phase2] !pop2 & push2 & buf2 < cap2 -> (buf2'=buf2+1);
[phase2] pop2 & !push2 & buf2 > 0 -> (buf2'=buf2-1);

endmodule


module buffer3

buf3 : [0..cap3] init 0;

[phase2] (pop3 & push3) | (!pop3 & !push3) -> (buf3'=buf3);
[phase2] !pop3 & push3 & buf3 < cap3 -> (buf3'=buf3+1);
[phase2] pop3 & !push3 & buf3 > 0 -> (buf3'=buf3-1);

endmodule


module buffer4

buf4 : [0..cap4] init 0;

[phase2] (pop4 & push4) | (!pop4 & !push4) -> (buf4'=buf4);
[phase2] !pop4 & push4 & buf4 < cap4 -> (buf4'=buf4+1);
[phase2] pop4 & !push4 & buf4 > 0 -> (buf4'=buf4-1);

endmodule


module buffer5 // SPECIAL

buf5 : [0..cap5] init cap5;
stack : [0..pallets-cap5] init pallets-cap5;

[phase1] stack>0 & buf5<cap5-1 -> (stack'=stack-1)&(buf5'=buf5+1);
[phase1] stack=0 | buf5>cap5-2 -> (stack'=stack);

[phase2] (pop5 & push5) | (!pop5 & !push5) -> (buf5'=buf5);
[phase2] !pop5 & push5 & buf5 < cap5 -> (buf5'=buf5+1);
[phase2] pop5 & !push5 & buf5 > 0 -> (buf5'=buf5-1);

endmodule


module machine1

pop5 : bool init false;
push1 : bool init false;
is_up1: [0..1] init 1;

[phase1] is_up1=1 & (buf1<cap1 & buf5>0) -> p1:(is_up1'=0)&(pop5'=true)&(push1'=false) + (1-p1):(is_up1'=1)&(pop5'=true)&(push1'=true);
[phase1] is_up1=0 -> r1:(is_up1'=1)&(pop5'=false)&(push1'=true) + (1-r1):(is_up1'=0)&(pop5'=false)&(push1'=false);
[phase1] is_up1=1 & (buf5=0 | buf1=cap1) -> (is_up1'=1)&(pop5'=false)&(push1'=false);

[phase2] true -> (pop5'=false)&(push1'=false);

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


module machine3

pop2 : bool init false;
push3 : bool init false;
is_up3: [0..1] init 1;

[phase1] is_up3=1 & (buf3<cap3 & buf2>0) -> p3:(is_up3'=0)&(pop2'=true)&(push3'=false) + (1-p3):(is_up3'=1)&(pop2'=true)&(push3'=true);
[phase1] is_up3=0 -> r3:(is_up3'=1)&(pop2'=false)&(push3'=true) + (1-r3):(is_up3'=0)&(pop2'=false)&(push3'=false);
[phase1] is_up3=1 & (buf2=0 | buf3=cap3) -> (is_up3'=1)&(pop2'=false)&(push3'=false);

[phase2] true -> (pop2'=false)&(push3'=false);

endmodule


module machine4

pop3 : bool init false;
push4 : bool init false;
is_up4: [0..1] init 1;

[phase1] is_up4=1 & (buf4<cap4 & buf3>0) -> p4:(is_up4'=0)&(pop3'=true)&(push4'=false) + (1-p4):(is_up4'=1)&(pop3'=true)&(push4'=true);
[phase1] is_up4=0 -> r4:(is_up4'=1)&(pop3'=false)&(push4'=true) + (1-r4):(is_up4'=0)&(pop3'=false)&(push4'=false);
[phase1] is_up4=1 & (buf3=0 | buf4=cap4) -> (is_up4'=1)&(pop3'=false)&(push4'=false);

[phase2] true -> (pop3'=false)&(push4'=false);

endmodule


module machine5

pop4 : bool init false;
push5 : bool init false;
is_up5: [0..1] init 1;

[phase1] is_up5=1 & (buf5<cap5 & buf4>0) -> p5:(is_up5'=0)&(pop4'=true)&(push5'=false) + (1-p5):(is_up5'=1)&(pop4'=true)&(push5'=true);
[phase1] is_up5=0 -> r5:(is_up5'=1)&(pop4'=false)&(push5'=true) + (1-r5):(is_up5'=0)&(pop4'=false)&(push5'=false);
[phase1] is_up5=1 & (buf4=0 | buf5=cap5) -> (is_up5'=1)&(pop4'=false)&(push5'=false);

[phase2] true -> (pop4'=false)&(push5'=false);

endmodule


rewards "WIP"

phase=1: 5 + buf1 + buf2 + buf3 + buf4 + buf5 - is_up1 - is_up2 - is_up3 - is_up4 -  is_up5 ;

endrewards




rewards "Production"

phase=2&push5: 1;

endrewards


rewards "Production_rate"

phase=2&push5: 2/timer;

endrewards

rewards "Starved2"

 phase=1&buf1=0: 2/timer;

endrewards


rewards "Starved3"

 phase=1&buf2=0: 2/timer;

endrewards



rewards "Blocked1"

 phase=1&buf1=cap1: 2/timer;

endrewards



rewards "Blocked2"

 phase=1&buf2=cap2: 2/timer;

endrewards


rewards "Broken1"

phase=1&is_up1=0: 2/timer;

endrewards

rewards "Broken2"

phase=1&is_up2=0: 2/timer;

endrewards

rewards "Broken3"

phase=1&is_up3=0: 2/timer;

endrewards

