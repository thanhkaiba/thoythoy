import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { ProductController } from './products.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductService } from './products.service';
import { Product } from './models/product.entity';



@Module({
  imports: [
    TypeOrmModule.forRoot({
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "username": "root",
      "password": "root",
      "database": "online_store",
      "entities": ["dist/**/*.entity{.ts,.js}"],
      "synchronize": true
  }),
  TypeOrmModule.forFeature([Product])
  ],
  controllers: [AppController, ProductController],
  providers: [ProductService],
})
export class AppModule {}
