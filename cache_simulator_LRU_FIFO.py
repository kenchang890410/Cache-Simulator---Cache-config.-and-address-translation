from posixpath import split
import math 
path='output.txt'
w=open(path, 'w')
f=open('2way_input.txt','r')
count_line=0
for line in f.readlines():
    if count_line==0:
        bit_tmp=line.split("  ")
        bit=bit_tmp[1]
        bit=bit.removesuffix('\n')
        count_line+=1
        continue
    elif count_line==1:
        cache_size_tmp=line.split(" ")
        cache_size=cache_size_tmp[2]
        count_line+=1
        cache_size=cache_size.removesuffix('\n')
        continue
    elif count_line==2:
        way_tmp=line.split(" ")
        way=way_tmp[1]
        way=way.removesuffix('\n')
        count_line+=1
        continue
    elif count_line==3:
        block_size_tmp=line.split(" ")
        block_size=block_size_tmp[2]
        block_size=block_size.removesuffix('\n')
        count_line+=1
        continue
    elif count_line==4:
        sets=(int(cache_size)*(2**10)/int(block_size))/int(way)#count sets
        index_bits=math.log2(sets) #count index bits
        block_offset=math.log2(int(block_size))#count offset bits
        tag_bits=int(bit)-index_bits-block_offset#count tag bits
        cache_tag=[[0]*int(way)for i in range (int(sets))]#build cache
        lru_table=[[0]*int(way)for j in range (int(sets))]#build lru table for count least recently used
        lru_switch=1 # 0=fifo,1=lru
        hit_count=0 #count hit rate
        miss_count=0#count miss rate
        hit_table_count=0#count lru 
        hit_table=[0]*100000#build for output
        count_line+=1
        continue
    else:
        line=line.removesuffix('\n')
        adress_tmp=line.split(" ")
        adress=adress_tmp[1]
        adress_dec=int(adress,16)
        adress_bin=format(adress_dec,"b")
        adress_bin_full=adress_bin.zfill(int(bit))
        adress_tag=adress_bin_full[int(tag_bits):int(-block_offset)]
        cache_index=int(adress_tag,2)
        for k in range(int(way)):
            if(cache_tag[int(cache_index)][k]==adress_bin_full[:int(tag_bits)]) and (cache_tag[int(cache_index)][k]!=0):#if hit
                if(lru_switch==1):
                    lru_table[int(cache_index)][k]=hit_table_count#renew count for lru
                if(k==0):
                    if int(cache_index)==0:
                        hit_table[hit_count]=str(line)+" hit set: 0 way: 0"
                    else:
                        hit_table[hit_count]=str(line)+" hit set: "+hex(cache_index)+" way: 0"
                else:
                    if int(cache_index)==0:
                        hit_table[hit_count]=str(line)+" hit set: 0 way: "+hex(k)
                    else:
                        hit_table[hit_count]=str(line)+" hit set: "+hex(cache_index)+" way: "+hex(k)#record output
                hit_count+=1
                break
            elif (cache_tag[int(cache_index)][k]==0):
                cache_tag[int(cache_index)][k]=adress_bin_full[:int(tag_bits)]#put tag to index
                lru_table[int(cache_index)][k]=hit_table_count#renew count for lru
                miss_count+=1
                break
            elif k==int(way)-1 :
                lru_min=1000000000#for count minimum use time
                replace_count=0#record which is lru
                for i in range(int(way)):
                    if lru_table[int(cache_index)][i]<lru_min:#find lru tag
                        replace_count=i
                        lru_min=lru_table[int(cache_index)][i]
                cache_tag[int(cache_index)][replace_count]=adress_bin_full[:int(tag_bits)]#kick lru tag and put tag to index
                lru_table[int(cache_index)][replace_count]=hit_table_count#renew count for lru
                miss_count+=1
        hit_table_count+=1#record lru number
    count_line+=1
print("num_set:",int(sets), file=w)#for print output
print("num_block_offset_bit:",int(block_offset), file=w)
print("num_index_bit:",int(index_bits), file=w)
print("num_tag_bit:",int(tag_bits), file=w)
print("num_total_access:",hit_table_count, file=w)
print("num_hit:",hit_count, file=w)
print("num_miss:",miss_count, file=w)
print("hit_rate:",math.floor(((hit_count/(miss_count+hit_count))*100)*100)/100.0,"%\n", file=w) 
print("hit trace:\n", file=w)
for i in range(hit_count):
    print(hit_table[i], file=w)
w.close()
f.close()
