SCRIPT_DTMC = 'dtmc\n'

SCRIPT_P = 'const double p{0} = {1};\n'
SCRIPT_R = 'const double r{0} = {1};\n'
SCRIPT_C = 'const int cap{0} = {1};\n'

SCRIPT_CONTROL = '''
module control

phase : [1..2] init 1;

[phase1] phase=1 -> (phase'=2);
[phase2] phase=2 -> (phase'=1);

endmodule
'''

SCRIPT_BUFFER_IN_OUT = 'const int buf{0} = 1;\n'

SCRIPT_BUFFER_MIDDLE = '''
module buffer{0}

buf{0} : [0..cap{0}] init 0;

[phase2] (pop{0} & push{0}) | (!pop{0} & !push{0}) -> (buf{0}'=buf{0});
[phase2] !pop{0} & push{0} & buf{0} < cap{0} -> (buf{0}'=buf{0}+1);
[phase2] pop{0} & !push{0} & buf{0} > 0 -> (buf{0}'=buf{0}-1);

endmodule
'''

SCRIPT_BUFFER_SPECIAL = '''
module buffer{0} // SPECIAL

buf{0} : [0..cap{0}] init cap{0};
stack : [0..pallets-cap{0}] init pallets-cap{0};

[phase1] stack>0 & buf{0}<cap{0}-1 -> (stack'=stack-1)&(buf{0}'=buf{0}+1);
[phase1] stack=0 | buf{0}>cap{0}-2 -> (stack'=stack);

[phase2] (pop{0} & push{0}) | (!pop{0} & !push{0}) -> (buf{0}'=buf{0});
[phase2] !pop{0} & push{0} & buf{0} < cap{0} -> (buf{0}'=buf{0}+1);
[phase2] pop{0} & !push{0} & buf{0} > 0 -> (buf{0}'=buf{0}-1);

endmodule
'''

SCRIPT_MACHINE_FIRST = '''
module machine{0}

push{0} : bool init false;
is_up{0}: [0..1] init 1;

[phase1] is_up{0}=1 & buf{0}<cap{0} -> p{0}:(is_up{0}'=0)&(push{0}'=false) + (1-p{0}):(is_up{0}'=1)&(push{0}'=true);
[phase1] is_up{0}=0 -> r{0}:(is_up{0}'=1)&(push{0}'=true) + (1-r{0}):(is_up{0}'=0)&(push{0}'=false);
[phase1] is_up{0}=1 & buf{0}=cap{0} -> (is_up{0}'=1)&(push{0}'=false);

[phase2] true -> (push{0}'=false);

endmodule
'''

SCRIPT_MACHINE_MIDDLE = '''
module machine{0}

pop{1} : bool init false;
push{0} : bool init false;
is_up{0}: [0..1] init 1;

[phase1] is_up{0}=1 & (buf{0}<cap{0} & buf{1}>0) -> p{0}:(is_up{0}'=0)&(pop{1}'=true)&(push{0}'=false) + (1-p{0}):(is_up{0}'=1)&(pop{1}'=true)&(push{0}'=true);
[phase1] is_up{0}=0 -> r{0}:(is_up{0}'=1)&(pop{1}'=false)&(push{0}'=true) + (1-r{0}):(is_up{0}'=0)&(pop{1}'=false)&(push{0}'=false);
[phase1] is_up{0}=1 & (buf{1}=0 | buf{0}=cap{0}) -> (is_up{0}'=1)&(pop{1}'=false)&(push{0}'=false);

[phase2] true -> (pop{1}'=false)&(push{0}'=false);

endmodule
'''

SCRIPT_MACHINE_LAST = '''
module machine{0}

pop{1} : bool init false;
is_up{0}: [0..1] init 1;

[phase1] is_up{0}=1 & buf{1}>0 -> p{0}:(is_up{0}'=0)&(pop{1}'=true) + (1-p{0}):(is_up{0}'=1)&(pop{1}'=true);
[phase1] is_up{0}=0 -> r{0}:(is_up{0}'=1)&(pop{1}'=false) + (1-r{0}):(is_up{0}'=0)&(pop{1}'=false);
[phase1] is_up{0}=1 & buf{1}=0 -> (is_up{0}'=1)&(pop{1}'=false);

[phase2] true -> (pop{1}'=false);

endmodule
'''

N = 5
p = [0.01]*N
r = [0.1]*N
c = [5]*(N-1)

mode = 2
SCRIPT_GLOBAL, SCRIPT_MODULES = '', ''

if mode == 0:
    SCRIPT_GLOBAL = SCRIPT_DTMC + '\n' + ''.join([
                        SCRIPT_P.format(i, p[i-1]) for i in range(1, N+1)
                    ]) + '\n' + ''.join([
                        SCRIPT_R.format(i, r[i-1]) for i in range(1, N+1)
                    ]) + '\n' + ''.join([
                        SCRIPT_C.format(i, c[i-1]) for i in range(1, N)
                    ]) + '\n'
                    
    SCRIPT_MODULES = SCRIPT_CONTROL + '\n'.join([
                        SCRIPT_BUFFER_MIDDLE.format(i) for i in range(1, N)
                    ]) + '\n' + SCRIPT_MACHINE_FIRST.format(1) + '\n'.join([
                        SCRIPT_MACHINE_MIDDLE.format(i, i-1) for i in range(2, N)
                    ]) + '\n' + SCRIPT_MACHINE_LAST.format(N, N-1)

elif mode == 1:
    SCRIPT_GLOBAL = SCRIPT_DTMC + '\n' + ''.join([
                        SCRIPT_P.format(i, p[i-1]) for i in range(1, N+1)
                    ]) + '\n' + ''.join([
                        SCRIPT_R.format(i, r[i-1]) for i in range(1, N+1)
                    ]) + '\n' + SCRIPT_C.format(0, 2) + ''.join([
                        SCRIPT_C.format(i, c[i-1]) for i in range(1, N)
                    ]) + SCRIPT_C.format(N, 2) + '\n'
                    
    SCRIPT_MODULES = SCRIPT_CONTROL + '\n' + SCRIPT_BUFFER_IN_OUT.format(0) + '\n'.join([
                        SCRIPT_BUFFER_MIDDLE.format(i) for i in range(1, N)
                    ]) + '\n' + SCRIPT_BUFFER_IN_OUT.format(N) + '\n' + '\n'.join([
                        SCRIPT_MACHINE_MIDDLE.format(i, i-1) for i in range(1, N+1)
                    ]) + '\n'

elif mode == 2:
    c += [5]
    pallets = 20
    
    SCRIPT_START = f'const int pallets = {pallets};\n'
    
    SCRIPT_GLOBAL = SCRIPT_DTMC + '\n' + ''.join([
                        SCRIPT_P.format(i, p[i-1]) for i in range(1, N+1)
                    ]) + '\n' + ''.join([
                        SCRIPT_R.format(i, r[i-1]) for i in range(1, N+1)
                    ]) + '\n' + ''.join([
                        SCRIPT_C.format(i, c[i-1]) for i in range(1, N+1)
                    ]) + '\n' + SCRIPT_START + '\n'
                    
    SCRIPT_MODULES = SCRIPT_CONTROL + '\n' + '\n'.join([
                        SCRIPT_BUFFER_MIDDLE.format(i) for i in range(1, N)
                    ]) + '\n' + SCRIPT_BUFFER_SPECIAL.format(N, 'plates') + '\n' + SCRIPT_MACHINE_MIDDLE.format(1, N) + '\n' + '\n'.join([
                        SCRIPT_MACHINE_MIDDLE.format(i, i-1) for i in range(2, N+1)
                    ]) + '\n'

with open('3machines.pm', 'w') as f: f.write(SCRIPT_GLOBAL + '\n' + SCRIPT_MODULES)