import math
import random

##数据生成函数，按照要求投掷N次生成结果，方便后面调用
def get_data(s,q,N):   

    data = []
    for i in range(N):      ##先选择是哪个球
        b_which = random.randint(1,100)
        if 1 <= b_which <= 100 * s[0]:  
            ball = 1
        elif b_which <= 100 * (s[0] + s[1]):
            ball = 2
        else:
            ball = 3

        b_direction = random.randint(1,100)
        if ball == 1:       ##计算选定球正面或者反面
            if 1 <= b_direction <= 100 * q[0]:
                data.append(1)
            else:
                data.append(0)
        elif ball == 2:
            if 1 <= b_direction <= 100 * q[1]:
                data.append(1)
            else:
                data.append(0)
        else:
            if 1 <= b_direction <= 100 * q[2]:
                data.append(1)
            else:
                data.append(0)  
    return data       

def piay_e(s,q,x):      ##做e步计算，根据公式进行计算即可

    u1_x, u2_x, u3_x = [], [], []

    for i in range(len(x)):
        if x[i] == 1:
            s0 = s[0]*q[0]
            s1 = s[1]*q[1]
            s2 = s[2]*q[2]
        else:
            s0 = s[0]*(1-q[0])
            s1 = s[1]*(1-q[1])
            s2 = s[2]*(1-q[2]) 
        s_all = s0 + s1 + s2
        u1_x.append(s0 / s_all)
        u2_x.append(s1 / s_all)
        u3_x.append(s2 / s_all)

    return [u1_x, u2_x, u3_x]

def play_m(u,x):        ##做m步计算，根据公式进行计算

    s = []
    q = []
    for j in range(3):

        s.append(sum(u[j])/len(u[j]))
        q.append(sum([u[j][i] * x[i] for i in range(len(x))])/sum(u[j]))

    return s, q

def play_em(s, q, x, N):        ##将上面两个函数结合，做迭代计算

    s_pre = s
    q_pre = q
    for i in range(N):
        u = piay_e(s_pre,q_pre,x)
        s_exp,q_exp = play_m(u,x)

        #迭代结束条件
        if sum([abs(q_pre[j] - q_exp[j]) for j in range(3)]) + sum([abs(s_pre[k] - s_exp[k]) for k in range(3)]) < 0.0000001:
            break

        s_pre = s_exp
        q_pre = q_exp
        
    return s_exp,q_exp,i+1




if __name__ == "__main__":

    s = [0.5,0.3,0.2]       #设定正确值，即为真值，
    q = [0.3,0.5,0.5]       
    N = 1000                #投掷1000次硬币
    x = get_data(s,q,N)     #生成结果

    s_start = [0.6,0.2,0.2] #迭代开始数据
    q_start = [0.2,0.4,0.4] #迭代开始数据

    s_pre,q_pre,i = play_em(s_start, q_start, x, N) #利用em算法做迭代

    print("迭代次数",i)
    print("迭代得到的各个硬币占比：",s_pre[0], s_pre[1], s_pre[2])
    print("初始的的各个硬币占比：",s[0], s[1], s[2])   
    print("迭代得到的各个硬币正面比例：",q_pre[0], q_pre[1], q_pre[2])
    print("初始设定得到的各个硬币正面比例：",q[0], q[1], q[2])

