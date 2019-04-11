#include<bits/stdc++.h>
using namespace std;
const int N=1000+10;
int a[N];
int u[N],v[N];
int dep[N];
int cnt,p,k;
bool vis[N];
string s;
int dfs()
{
	int val=s[p]-'0';
	a[cnt]=val;
	int now=cnt;
	cnt+=5;
	p++;
	int son[N];
	int num=0;
	while(1)
	{
		if(s[p]==')')
		{
			if(num) vis[now]=true;
			for(int i=0;i<num;i++)
			{
				u[k]=son[i];
				v[k]=now;
				k++;
			}
			return now;
		}
		if(s[p]=='(')
		{
			p++;
			son[num++]=dfs();
			dep[now]=max(dep[now],dep[son[num-1]]+1);
		}
		p++;
	}
	return now;
}
int sum[10];
int main()
{
	freopen("all_tree.txt","r",stdin);
	freopen("treebank_graph_small.txt","w",stdout);
	int graph_cnt1=0,graph_cnt2=0;
	//for train
	memset(sum,0,sizeof(sum));
	while(getline(cin,s))
	{
		bool flag=false;
		for(int i=0;i<5;i++)
			if(sum[i]<500) flag=true;
		if(!flag) break;

		memset(dep,0,sizeof(dep));		
		memset(vis,false,sizeof(vis));
		p=1;
		k=0;
		cnt=1;

		int root=dfs();

		flag=false;
		for(int i=1;i<cnt;i+=5)
			if(sum[a[i]]<500) flag=true;
		if(!flag) continue;
		graph_cnt1++;

		for(int i=0;i<k;i++)
		{
			for(int j1=0;j1<5;j1++)
				for(int j2=0;j2<5;j2++)
					printf("%d %d %d\n",u[i]+j1,j1*5+j2+1,v[i]+j2);
		}

		printf("!");
		for(int i=1;i<cnt;i+=5)
		{
			if(!vis[i])
			{
				for(int j=0;j<5;j++)
					if(a[i]==j) printf(" 1");
					else printf(" 0");
			}
			else for(int j=0;j<5;j++) printf(" 0");
		}
		printf("\n");

		//printf("? 1 1 %d %d\n",dep[1],a[1]+1);
		//continue;

		for(int i=1;i<cnt;i+=5)
		{
			if(sum[a[i]]>500) continue;
			sum[a[i]]++;
			printf("? 1 %d %d %d\n",i,dep[i],i+a[i]);
		}
		printf("\n");
	}
	//for test
	memset(sum,0,sizeof(sum));
	while(getline(cin,s))
	{
		bool flag=false;
		for(int i=0;i<5;i++)
			if(sum[i]<100) flag=true;
		if(!flag) break;

		memset(dep,0,sizeof(dep));		
		memset(vis,false,sizeof(vis));
		p=1;
		k=0;
		cnt=1;

		int root=dfs();

		flag=false;
		for(int i=1;i<cnt;i+=5)
			if(sum[a[i]]<100) flag=true;
		if(!flag) continue;
		graph_cnt2++;

		for(int i=0;i<k;i++)
		{
			for(int j1=0;j1<5;j1++)
				for(int j2=0;j2<5;j2++)
					printf("%d %d %d\n",u[i]+j1,j1*5+j2+1,v[i]+j2);
		}

		printf("!");
		for(int i=1;i<cnt;i+=5)
		{
			if(!vis[i])
			{
				for(int j=0;j<5;j++)
					if(a[i]==j) printf(" 1");
					else printf(" 0");
			}
			else for(int j=0;j<5;j++) printf(" 0");
		}
		printf("\n");

		//printf("? 1 1 %d %d\n",dep[1],a[1]+1);
		//continue;

		for(int i=1;i<cnt;i+=5)
		{
			if(sum[a[i]]>100) continue;
			sum[a[i]]++;
			printf("? 1 %d %d %d\n",i,dep[i],i+a[i]);
		}
		printf("\n");
	}

	freopen("CON","w",stdout);
	printf("%d %d\n",graph_cnt1,graph_cnt2);
	return 0;
}