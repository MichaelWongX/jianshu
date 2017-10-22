# jianshu
jianshu spider
一个基于scrapy框架的简书爬虫，可结合redis进行分布式爬取（scrapy-redis框架)和使用mongodb进行item存储。
测试环境1：win10 X64，miniconda3 虚拟环境，python3.5.4 或者python3.6.2

测试环境2：centos7.3 X64,aliyun ECS, miniconda3，python3.5.4

    
      
说明：
1. 工程中包含一个CrawlSpider扩展类JianshulaSpider，使用四条Rule分别进行文章、关注者、粉丝、个人信息解析；

          class JianshulaSpider(CrawlSpider):
                  name = 'jianshula'
                  allowed_domains = ['jianshu.com']
                  start_urls = ['http://www.jianshu.com/']

              rules = (
                  Rule(LinkExtractor(allow=r'/p/'), callback='parse_article', follow=True),
                  Rule(LinkExtractor(allow=r'/users/[0-9a-z]*/following'), callback='parse_following', follow=True),
                  Rule(LinkExtractor(allow=r'/users/[0-9a-z]*/followers'), callback='parse_fans', follow=True),
                  Rule(LinkExtractor(allow=r'/u/[0-9a-z]*'), callback='parse_author', follow=True),
              ）    
2. 继承HttpErrorMiddleware类，增加JianshuHttpErrorMiddleware类，以忽略简书大量404错误（文章被删除等）

        SPIDER_MIDDLEWARES = {
            'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware':None,
            'jianshu.middlewares.JianshuHttpErrorMiddleware': 50,
        }

3. 继承scrapy_monodb.MongoDBPipeline类，已修正在python3上的item.iteritems方法不错在的错误




