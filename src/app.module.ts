import { Global, Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { ProductController } from './products.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductService } from './products.service';
import { Product } from './models/product.entity';
import { AdminModule } from './admin/admin.module';
import { User } from './models/user.entity';
import { AuthModule } from './auth/auth.module';
import { UsersService } from './models/users.service';

@Global()
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'localhost',
      port: 3306,
      username: 'root',
      password: 'root',
      database: 'online_store',
      entities: ['dist/**/*.entity{.ts,.js}'],
      synchronize: true,
    }),
    TypeOrmModule.forFeature([Product, User]),
    AdminModule,
    AuthModule,
  ],
  controllers: [AppController, ProductController],
  providers: [ProductService, UsersService],
  exports: [ProductService, UsersService]
})
export class AppModule {}
