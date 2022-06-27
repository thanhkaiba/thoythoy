import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { ProductController } from './product.controller';

@Module({
  imports: [],
  controllers: [AppController, ProductController],
  providers: [],
})
export class AppModule {}
